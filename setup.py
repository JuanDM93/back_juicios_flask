#TESTS
#pip install '.[test]'
#pytest
from setuptools import find_packages, setup

setup(
    name='api',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_mysqldb',
        'flask_cors',
        'flask_bcrypt',
        'flask_jwt_extended',
        'Flask-Mail',
        'Flask-APScheduler',
        'tika',     # java required
    ],
)