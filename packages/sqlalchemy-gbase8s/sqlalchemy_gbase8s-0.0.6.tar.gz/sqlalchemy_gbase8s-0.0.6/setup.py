from setuptools import setup

setup(
    entry_points={
        'sqlalchemy.dialects': [
            'gbase8s = sqlalchemy_gbase8s.ibmdb:GBase8sDialect',
        ]
    }
)
