__version__ = '0.0.6'

import os
from sqlalchemy.dialects import registry

os.environ['DELIMIDENT'] = 'y'

registry.register("gbase8s", "sqlalchemy_gbase8s.ibmdb", "GBase8sDialect")
