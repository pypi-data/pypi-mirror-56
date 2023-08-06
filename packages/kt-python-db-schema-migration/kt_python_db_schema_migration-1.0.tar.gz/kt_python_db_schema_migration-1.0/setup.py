from setuptools import setup, find_packages

install_requires = []

setup(
    name='kt_python_db_schema_migration',
    version='1.0',
    url='http://github.com/k-t-corp/python-db-schema-migration',
    author='KTachibanaM',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    test_suite="python_db_schema_migration_tests",
)
