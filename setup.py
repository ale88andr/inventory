from distutils.core import setup
from inventory import __version__ as version
from inventory import __appname__ as appname

setup(
    name=appname,
    version=version,
    packages=['inventory'],
    url='',
    license='MIT',
    author='Alexandr Nekrasov',
    author_email='ale88andr@gmail.com',
    description='Inventory service',
    requires=['django']
)
