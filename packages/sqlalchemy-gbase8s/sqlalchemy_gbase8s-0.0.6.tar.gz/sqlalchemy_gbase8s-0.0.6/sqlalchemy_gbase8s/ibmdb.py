from contextlib import contextmanager
from decimal import Decimal, localcontext
from functools import reduce
from itertools import groupby
import re

import ibm_db_dbi as Database
import pyodbc

from sqlalchemy import exc, sql, types, util, schema
from sqlalchemy.sql import compiler, sqltypes
from sqlalchemy.engine import default, reflection

from urllib import parse
import logging

error_re = re.compile(r'SQLCODE=-(\d+)')


AUTOCOMMIT_RE = re.compile(r'\s*(?:UPDATE|INSERT|CREATE|DELETE|DROP|ALTER)', re.I | re.UNICODE)


ischema_names = {
    0: sqltypes.CHAR,           # CHAR
    1: sqltypes.SMALLINT,       # SMALLINT
    2: sqltypes.INTEGER,        # INT
    3: sqltypes.FLOAT,          # Float
    4: sqltypes.Float,          # SmallFloat
    5: sqltypes.DECIMAL,        # DECIMAL
    6: sqltypes.Integer,        # Serial
    7: sqltypes.DATE,           # DATE
    8: sqltypes.Numeric,        # MONEY
    10: sqltypes.DATETIME,      # DATETIME
    11: sqltypes.LargeBinary,   # BYTE
    12: sqltypes.TEXT,          # TEXT
    13: sqltypes.VARCHAR,       # VARCHAR
    15: sqltypes.NCHAR,         # NCHAR
    16: sqltypes.NVARCHAR,      # NVARCHAR
    17: sqltypes.Integer,       # INT8
    18: sqltypes.Integer,       # Serial8
    43: sqltypes.String,        # LVARCHAR
    114: sqltypes.Integer,        # know type by jacky
}


@contextmanager
def wrap_ibm_db_errors(statement, params):
    try:
        yield
    except Database.OperationalError as e:
        error = int(error_re.search(e._message).groups()[0])
        errors = [268, 691, 530, 391]
        if error in errors:
            raise exc.IntegrityError(statement, params, e) from e
        raise


class GBase8sNumeric(types.Numeric):
    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            if self.asdecimal:
                if not isinstance(value, Decimal):
                    with localcontext() as ctx:
                        ctx.prec = 10
                        value = ctx.create_decimal_from_float(value)
            else:
                value = float(value)

            return value

        return process

    def literal_processor(self, dialect):
        def process(value):
            if isinstance(value, float):
                return '%s::float' % str(value)
            return str(value)

        return process


class GBase8sBoolean(types.Boolean):
    def result_processor(self, dialect, coltype):
        def process(value):
            return bool(value) if value is not None else None

        return process


class GBase8sTime(types.Time):
    def result_processor(self, dialect, coltype):
        def process(value):
            return value.time() if value is not None else None

        return process


class GBase8sTypeCompiler(compiler.GenericTypeCompiler):
    def visit_TEXT(self, type_):
        return self.visit_CLOB(type_)

    def visit_DATETIME(self, type_):
        return 'DATETIME YEAR TO FRACTION'

    def visit_TIME(self, type_):
        return 'DATETIME HOUR TO FRACTION'


class GBase8sCompiler(compiler.SQLCompiler):
    ansi_bind_rules = True

    def default_from(self):
        return ' FROM sysmaster:sysdual'

    def visit_true(self, element, **kw):
        return "'t'"

    def visit_false(self, element, **kw):
        return "'f'"

    def visit_sequence(self, seq):
        return "%s.NEXTVAL" % self.preparer.format_sequence(seq)

    def get_select_precolumns(self, select, **kw):
        """Called when building a ``SELECT`` statement, position is just
        before column list GBase8s puts the limit and offset right
        after the ``SELECT``...
        """

        result = ""
        if select._offset_clause is not None:
            result += "SKIP %s " % select._offset
        if select._limit_clause is not None:
            result += "FIRST %d " % select._limit
        if select._distinct:
            result += "DISTINCT "
        return result

    def limit_clause(self, select, **kw):
        """Already taken care of in the `get_select_precolumns` method."""
        return ""


class GBase8sExecutionContext(default.DefaultExecutionContext):
    _select_lastrowid = False
    _lastrowid = None

    def _is_serial_col(self, column):
        return (column is not None and column.primary_key
                and column is column.table._autoincrement_column and
                (column.default is None or (isinstance(column.default, schema.Sequence) and column.default.optional)))

    def get_lastrowid(self):
        # print("GETTING LAST ROW ID")
        # print(self._lastrowid)
        return self._lastrowid

    def pre_exec(self):
        if self.isinsert and self._is_serial_col(self.compiled.statement.table._autoincrement_column):
            self._select_lastrowid = not self.compiled.returning and not self.compiled.inline

        return super().pre_exec()

    def post_exec(self):
        if self._select_lastrowid:
            # Massive hack to get the last inserted serial (sqlca.sqlerrd1) or bigserial
            # Apparently both are never set
            try:
                cursor = self.create_cursor()
                # fix by jacky can't use this sql below , but use ** select dbinfo('sqlca.sqlerrd1') from systables limit 1 **
                # print("SELECT dbinfo('sqlca.sqlerrd1'), dbinfo('bigserial') FROM sysmaster:sysdual")

                cursor.execute("select dbinfo('sqlca.sqlerrd1') from systables limit 1 ")
                result = cursor.fetchone()
                # assert(not all(result))
                # print(result[0])
                self._lastrowid = result[0] #+ result[1]
                # print(self._lastrowid)
            except Exception as e:
                print(e)

        return super().post_exec()

    def should_autocommit_text(self, statement):
        return AUTOCOMMIT_RE.match(statement)

    def fire_sequence(self, seq, type_):
        return self._execute_scalar(
            "SELECT " +
            self.dialect.identifier_preparer.format_sequence(seq) +
            ".NEXTVAL FROM sysmaster:sysdual", type_)


class GBase8sDDLCompiler(compiler.DDLCompiler):
    def get_column_specification(self, column, **kwargs):
        colspec = self.preparer.format_column(column)

        impl_type = column.type.dialect_impl(self.dialect)
        if isinstance(impl_type, sqltypes.TypeDecorator):
            impl_type = impl_type.impl

        if (column.primary_key and column is column.table._autoincrement_column and
                column.default is None or
                (isinstance(column.default, schema.Sequence) and column.default.optional)):
            if isinstance(impl_type, sqltypes.BigInteger):
                colspec += " BIGSERIAL"
            else:
                colspec += " SERIAL"
        else:
            colspec += " " + self.dialect.type_compiler.process(column.type, type_expression=column)
            default = self.get_column_default_string(column)
            if default is not None:
                    colspec += " DEFAULT " + default

        if not column.nullable:
            colspec += " NOT NULL"
        return colspec

    def _constraint_name(self, constraint):
        if 'TEMP' in constraint.table._prefixes:
            return ""  # No constraint names allowed for temp tables
        if constraint.name is not None:
            formatted_name = self.preparer.format_constraint(constraint)
            if formatted_name is not None:
                return " CONSTRAINT %s " % formatted_name
        else:
            return ""

    def visit_foreign_key_constraint(self, constraint):
        preparer = self.preparer
        text = ""
        remote_table = list(constraint.elements)[0].column.table
        text += "FOREIGN KEY(%s) REFERENCES %s (%s)" % (
            ', '.join(preparer.quote(f.parent.name)
                      for f in constraint.elements),
            self.define_constraint_remote_table(
                constraint, remote_table, preparer),
            ', '.join(preparer.quote(f.column.name)
                      for f in constraint.elements)
        )
        text += self.define_constraint_match(constraint)
        text += self.define_constraint_cascades(constraint)
        text += self._constraint_name(constraint)
        return text

    def visit_primary_key_constraint(self, constraint):
        if len(constraint) == 0:
            return ''
        text = "PRIMARY KEY "
        text += "(%s)" % ', '.join(self.preparer.quote(c.name)
                                   for c in (constraint.columns_autoinc_first
                                   if constraint._implicit_generated
                                   else constraint.columns))
        text += self._constraint_name(constraint)
        return text

    def visit_unique_constraint(self, constraint):
        if len(constraint) == 0:
            return ''
        text = "UNIQUE (%s)" % (
                ', '.join(self.preparer.quote(c.name)
                          for c in constraint))
        text += self._constraint_name(constraint)
        return text

    def visit_check_constraint(self, constraint):
        text = "CHECK (%s)" % self.sql_compiler.process(constraint.sqltext,
                                                         include_table=False,
                                                         literal_binds=True)
        text += self._constraint_name(constraint)
        return text

    def visit_create_table(self, create):
        table = create.element

        if table._prefixes == ['TEMPORARY']:
            table._prefixes[:] = ['TEMP']

        return super().visit_create_table(create)


class GBase8sDialect(default.DefaultDialect):
    name = 'gbase8s'
    driver = 'ibmdb'

    execution_ctx_cls = GBase8sExecutionContext

    statement_compiler = GBase8sCompiler
    type_compiler = GBase8sTypeCompiler
    ddl_compiler = GBase8sDDLCompiler

    supports_native_boolean = True
    supports_native_decimal = True

    supports_sequences = True
    postfetch_lastrowid = True

    # ec = ''
    # ecc = ''
    # ecw = ''

    colspecs = {
        types.Time: GBase8sTime,
        types.Boolean: GBase8sBoolean,
        types.Numeric: GBase8sNumeric
    }

    def __init__(self, isolation_level=None, **kwargs):
        super().__init__(self, **kwargs)
        self.isolation_level = isolation_level

        self.ec = ''
        self.ecc = ''
        self.ecw = ''

    def on_connect(self):
        def connect(conn):
            cursor = conn.cursor()
            cursor.execute("SELECT is_logging FROM sysmaster:sysdatabases WHERE name=DBINFO('dbname')")
            result = cursor.fetchone()
            cursor.close()
            # conn.has_transactions = bool(result[0])

            if self.isolation_level is not None:
                self.set_isolation_level(conn, self.isolation_level)

        return connect

    def connect(self, *cargs, **cparams):
        # print("running !!!!")
        # print(cargs)
        # print(cargs[0])
        # print("running !!!!")
        #;UID=gbasedbt;PWD=GBase00!
        conn = pyodbc.connect(cargs[0])
        # conn = pyodbc.connect('DRIVER={/opt/gbase8s/lib/cli/iclis09b.so};SERVER=gbaseserver;PORT=9088;DATABASE=gbasedb;UID=gbasedbt;PWD=GBase00!;CHARSET=UTF8')
        conn.autocommit = True

        logging.debug('ec = ')
        if self.ec == '' or self.ec is None:
            logging.debug('kong')
            conn.setencoding(encoding='UTF-8')
        else:
            logging.debug(self.ec)
            conn.setencoding(encoding=self.ec)

        logging.debug('ecw = ')
        if self.ecw == '' or self.ecw is None:
            logging.debug('kong')
            conn.setdecoding(pyodbc.SQL_WCHAR, encoding='UTF-8')
        else:
            logging.debug(self.ecw)
            conn.setdecoding(pyodbc.SQL_WCHAR,encoding=self.ecw)

        logging.debug('ecc = ')
        if self.ecc == '' or self.ecc is None:
            logging.debug('kong')
            conn.setdecoding(pyodbc.SQL_CHAR, encoding='UTF-8')
        else:
            logging.debug(self.ecc)
            conn.setdecoding(pyodbc.SQL_CHAR,encoding=self.ecc)
        # conn.setencoding(encoding='UTF-8')
        # conn.setdecoding(pyodbc.SQL_WCHAR, encoding='UTF-8')
        # conn.setdecoding(pyodbc.SQL_CHAR, encoding='UTF-8')
        #return pyodbc.connect('DRIVER={/opt/gbase8s/lib/cli/iclis09b.so};SERVER=gbaseserver;PORT=9088;DATABASE=gbasedb;UID=gbasedbt;PWD=GBase00!;CHARSET=UTF8')
        return conn
    @classmethod
    def dbapi(cls):
        return Database

    def create_connect_args(self, url):
        # print(url.query)
        # add by jacky  only get DSN params to pre 8s odbc
        opts = url.translate_connect_args()
        {'database': 'mhilf', 'host': 'apo.bap.lan',
            'username': 'GBase8s', 'password': 'GBase8s', 'port': 9092, 'DSN': 'test'}
        connectors = []
        available_options = {
            'username': 'UID',
            'password': 'PWD',
            'host': 'HOSTNAME',
            'port': 'PORT',
            'database': 'DATABASE'
        }
        for sa_opt, ifx_opt in available_options.items():
            if sa_opt in opts:
                connectors.append('%s=%s' % (ifx_opt, opts[sa_opt]))
        connectors.append('PROTOCOL=TCPIP')
        dsnconnectors = []
        dsnconnectors.append('%s=%s' % ('DSN', url.query['DSN']))
        self.ec = url.query.get('ec')
        self.ecw = url.query.get('ecw')
        self.ecc = url.query.get('ecc')
        logging.debug([[''.join(dsnconnectors)], {}])
        return [[''.join(dsnconnectors)], {}]
    def _has_table_object(self, connection, objname, schema=None, type='T'):
        schema = schema or self.default_schema_name
        result = connection.scalar(
            sql.text("""SELECT count(*) FROM systables
                      WHERE tabname=:name AND owner=:schema AND tabtype=:type"""),
            name=objname, schema=schema, type=type
        )
        return bool(result)

    def has_table(self, connection, tablename, schema=None):
        return self._has_table_object(connection, tablename, schema, 'T')

    def has_sequence(self, connection, sequence_name, schema=None):
        return self._has_table_object(connection, sequence_name, schema, 'Q')

    def _get_default_schema_name(self, connection):
        return connection.scalar('SELECT CURRENT_USER FROM sysmaster:sysdual')

    def set_isolation_level(self, connection, level):
        # adjust for ConnectionFairy possibly being present
        if hasattr(connection, 'connection'):
            connection = connection.connection
        if level == 'AUTOCOMMIT':
            connection.set_autocommit(True)
        else:
            connection.set_autocommit(False)

    def do_executemany(self, cursor, statement, parameters, context=None):
        # At least inserts with execute_many seem to fail
        # SQLRowCount failed: [IBM][CLI Driver] CLI0125E  Function sequence error. SQLSTATE=HY010 SQLCODE=-99999
        # Also executemany needs homogenous types :/
        with wrap_ibm_db_errors(statement, parameters):
            for param in parameters:
                cursor.execute(statement, param)

    def do_execute(self, cursor, statement, parameters, context=None):
        with wrap_ibm_db_errors(statement, parameters):
            return cursor.execute(statement, parameters)

    def do_execute_no_params(self, cursor, statement, context=None):
        with wrap_ibm_db_errors(statement, []):
            return cursor.execute(statement)

    def do_rollback(self, dbapi_connection):
        #if dbapi_connection.has_transactions:
            dbapi_connection.rollback()

    def do_commit(self, dbapi_connection):
        # if dbapi_connection.has_transactions:
            dbapi_connection.commit()

    def do_close(self, dbapi_connection):
        try:
            dbapi_connection.close()
        except Database.Error as e:
            # Transactions not available during close does not hurt.
            if int(error_re.search(e._message).groups()[0]) != 256:
                raise

    def _get_table_names(self, connection, schema, type, **kw):
        schema = schema or self.default_schema_name
        s = """SELECT tabname, owner FROM systables WHERE owner=? AND tabtype=?"""
        return [row[0] for row in connection.execute(s, schema, type)]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        return self._get_table_names(connection, schema, 'T', **kw)

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        return self._get_table_names(connection, schema, 'V', **kw)

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        schema = schema or self.default_schema_name
        c = connection.execute(
            """SELECT colname, coltype, collength, t3.default, t1.colno FROM
                syscolumns AS t1 , systables AS t2 , OUTER sysdefaults AS t3
                WHERE t1.tabid = t2.tabid AND t2.tabname=? AND t2.owner=?
                  AND t3.tabid = t2.tabid AND t3.colno = t1.colno
                ORDER BY t1.colno""", table_name, schema)

        pk_constraint = self.get_pk_constraint(connection, table_name, schema, **kw)
        primary_cols = pk_constraint['constrained_columns']

        columns = []
        rows = c.fetchall()
        for name, colattr, collength, default, colno in rows:
            name = name.lower()

            autoincrement = False
            primary_key = False

            if name in primary_cols:
                primary_key = True

            # in 7.31, coltype = 0x000
            #                       ^^-- column type
            #                      ^-- 1 not null, 0 null
            not_nullable, coltype = divmod(colattr, 256)
            if coltype not in (0, 13) and default:
                default = default.split()[-1]

            if coltype == 6:  # Serial, mark as autoincrement
                autoincrement = True

            if coltype == 0 or coltype == 13:  # char, varchar
                coltype = ischema_names[coltype](collength)
                if default:
                    default = "'%s'" % default
            elif coltype == 5:  # decimal
                precision, scale = (collength & 0xFF00) >> 8, collength & 0xFF
                if scale == 255:
                    scale = 0
                coltype = sqltypes.Numeric(precision, scale)
            else:
                try:
                    coltype = ischema_names[coltype]
                except KeyError:
                    util.warn("Did not recognize type '%s' of column '%s'" %
                              (coltype, name))
                    coltype = sqltypes.NULLTYPE

            column_info = dict(name=name, type=coltype, nullable=not not_nullable,
                               default=default, autoincrement=autoincrement,
                               primary_key=primary_key)
            columns.append(column_info)
        return columns

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        schema_sel = schema or self.default_schema_name
        c = connection.execute(
        """SELECT t1.constrname AS cons_name,
                 t4.colname AS local_column, t7.tabname AS remote_table,
                 t6.colname AS remote_column, t7.owner AS remote_owner,
                 t5.delrule
            FROM sysconstraints AS t1 , systables AS t2 ,
                 sysindexes AS t3 , syscolumns AS t4 ,
                 sysreferences AS t5 , syscolumns AS t6 , systables AS t7 ,
                 sysconstraints AS t8 , sysindexes AS t9
           WHERE t1.tabid = t2.tabid AND t2.tabname=? AND t2.owner=? AND t1.constrtype = 'R'
             AND t3.tabid = t2.tabid AND t3.idxname = t1.idxname
             AND t4.tabid = t2.tabid AND t4.colno in (t3.part1, t3.part2, t3.part3,
             t3.part4, t3.part5, t3.part6, t3.part7, t3.part8, t3.part9, t3.part10,
             t3.part11, t3.part11, t3.part12, t3.part13, t3.part4, t3.part15, t3.part16)
             AND t5.constrid = t1.constrid AND t8.constrid = t5.primary
             AND t6.tabid = t5.ptabid AND t6.colno in (t9.part1, t9.part2, t9.part3,
             t9.part4, t9.part5, t9.part6, t9.part7, t9.part8, t9.part9, t9.part10,
             t9.part11, t9.part11, t9.part12, t9.part13, t9.part4, t9.part15, t9.part16) AND t9.idxname =
             t8.idxname
             AND t7.tabid = t5.ptabid""", table_name, schema_sel)

        def fkey_rec():
            return {
                 'name': None,
                 'constrained_columns': [],
                 'referred_schema': None,
                 'referred_table': None,
                 'referred_columns': [],
                 'options': {}
             }

        fkeys = util.defaultdict(fkey_rec)

        rows = c.fetchall()
        for cons_name, local_column, remote_table, remote_column, remote_owner, delrule in rows:

            rec = fkeys[cons_name]
            rec['name'] = cons_name
            local_cols, remote_cols = rec['constrained_columns'], rec['referred_columns']

            if not rec['referred_table']:
                rec['referred_table'] = remote_table
                if schema is not None:
                    rec['referred_schema'] = remote_owner

            if local_column not in local_cols:
                local_cols.append(local_column)
            if remote_column not in remote_cols:
                remote_cols.append(remote_column)
            if delrule == 'C':
                rec['options']['ondelete'] = 'CASCADE'

        return list(fkeys.values())

    @reflection.cache
    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        indexes = self.get_indexes(connection, table_name, schema, **kw)
        constraints = []
        for index in indexes:
            if index['unique']:
                constraints.append({
                    'name': index['constraint_name'],
                    'column_names': index['column_names']
                })

        return constraints

    @reflection.cache
    def get_check_constraints(self, connection, table_name, schema=None, **kw):
        schema = schema or self.default_schema_name

        c = connection.execute("""
            SELECT t1.*, t2.checktext FROM sysconstraints AS t1, syschecks AS t2
            WHERE t1.tabid = (SELECT tabid FROM systables WHERE tabname=? AND OWNER=?)
            AND t1.constrid = t2.constrid AND t2.type = 'T' AND t1.constrtype = 'C'
            ORDER BY t1.constrname, t2.seqno
        """, table_name, schema)

        constraints = []
        for k, g in groupby(c.fetchall(), lambda row: row.constrname):
            constraints.append({
                'name': k,
                'sqltext': ''.join(map(lambda row: row.checktext, g)).rstrip()
            })

        return constraints

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        schema = schema or self.default_schema_name

        # Select the column positions from sysindexes for sysconstraints
        data = connection.execute(
            """SELECT t2.*
            FROM systables AS t1, sysindexes AS t2, sysconstraints AS t3
            WHERE t1.tabid=t2.tabid AND t1.tabname=? AND t1.owner=?
            AND t2.idxname=t3.idxname AND t3.constrtype='P'""",
            table_name, schema
        ).fetchall()

        colpositions = set()

        for row in data:
            colpos = set([getattr(row, 'part%d' % x) for x in range(1, 16)])
            colpositions |= colpos

        if not len(colpositions):
            return {'constrained_columns': [], 'name': None}

        # Select the column names using the columnpositions
        # TODO: Maybe cache a bit of those col infos (eg select all colnames for one table)
        place_holder = ','.join('?' * len(colpositions))
        c = connection.execute(
            """SELECT t1.colname
            FROM syscolumns AS t1, systables AS t2
            WHERE t2.tabname=? AND t1.tabid = t2.tabid AND
            t1.colno IN (%s)""" % place_holder,
            table_name, *colpositions
        ).fetchall()

        cols = reduce(lambda x, y: list(x) + list(y), c, [])
        return {'constrained_columns': cols, 'name': None}

    @reflection.cache
    def get_indexes(self, connection, table_name, schema, **kw):
        schema = schema or self.default_schema_name
        c = connection.execute(
            """SELECT t1.*, t2.constrtype, t2.constrname
            FROM sysindexes AS t1 LEFT JOIN sysconstraints AS t2
                ON (t1.tabid = t2.tabid AND t1.idxname = t2.idxname)
            WHERE
            t1.tabid = (SELECT tabid FROM systables WHERE tabname=? AND OWNER=?)
            """,
             table_name, schema)

        indexes = []
        for row in c.fetchall():
            print(row)
            # by jack for  AttributeError: Could not locate column in row for column 'constrtype'
            # result as ('tabname', 'gbasedbt                        ', 1, 'U', '-', 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None, None, None, None, None, None)
            # TODO  : verify is it right ???
            # if row.constrtype == 'P':  # now i don't konw why couldn't use colName , so i change to use index
            if row[4] == 'P':  # Cannot filter in the statement above due to bug?
                continue
            #  colnos = [getattr(row, 'part%d' % x) for x in range(1, 17)]
            colnos = [row[2],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17]]
            # print(colnos)
            colnos = [abs(x) for x in colnos if x]
            place_holder = ','.join('?' * len(colnos))
            c = connection.execute(
                """SELECT t1.colno, t1.colname
                FROM syscolumns AS t1, systables AS t2
                WHERE t2.tabname=? AND t1.tabid = t2.tabid AND t2.owner = ? AND
                t1.colno IN (%s)""" % place_holder,
                table_name, schema, *colnos
            ).fetchall()
            mapping = dict(c)
            indexes.append({
                'name': row[1],
                'unique': row[3].lower() == 'u',
                'column_names': [mapping.get(no) for no in colnos],
                'constraint_name': row[26]
            })
        return indexes

    @reflection.cache
    def get_view_definition(self, connection, view_name, schema=None, **kw):
        schema = schema or self.default_schema_name
        c = connection.execute(
            """SELECT t1.viewtext
            FROM sysviews AS t1 , systables AS t2
            WHERE t1.tabid=t2.tabid AND t2.tabname=?
            AND t2.owner=? ORDER BY seqno""",
             view_name, schema).fetchall()

        return ''.join([row[0] for row in c])
