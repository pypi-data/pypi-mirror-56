# sqlalchemy-gbase8s

![](https://www.travis-ci.org/dafei1288/sqlalchemy-gbase8s.svg?branch=master)

本程序 fork from `https://gitlab.com/apollo13/sqlalchemy-informix`

程序发布在 `https://pypi.org/project/sqlalchemy-gbase8s/0.0.1/` 

使用odbc 与 gbase8s 进行连接,确保系统内 odbc正常

## 安装 unixODBC

centos/redhat系

`sudo yum install unixODBC-devel`

ubuntu

`sudo apt-get install unixodbc unixodbc-dev`


# 添加依赖

```
pip install sqlalchemy
pip install pyodbc
pip install ibm_db
pip install sqlalchemy-gbase8s
```

# 使用

## url

![](./doc/dburl.png)




# 开发者

## 测试

`pip install pytest`

用于测试整合pandas

`pip install pandas`  

## 环境变量

开发者如果出现无法读取系统环境变量导致odbc连接异常，可以通过设置启动环境变量将来规避此问题

```
LD_LIBRARY_PATH=/opt/gbase8s/lib:/opt/gbase8s/lib/esql:/opt/gbase8s/lib/cli;
ODBCINI=/opt/gbase8s/etc/odbc.ini;
GBASEDBTSERVER=ol_gbasedbt1210_1;
GBASEDBTDIR=/opt/gbase8s;
GBASEDBTSQLHOSTS=/opt/gbase8s/etc/sqlhosts.ol_gbasedbt1210_1;
ONCONFIG=onconfig.ol_gbasedbt1210_1;
DB_LOCALE=zh_CN.utf8;
CLIENT_LOCALE=zh_CN.utf8
```

## 新增特性

1. 支持整合 pandas   `df = pd.read_sql_query(self.session.query(T).statement,self.engine)`