from setuptools import setup, find_packages
import os
from taz._version import __version__


long_description = 'SEE README file'

# install is run by using: python setup.py install

# exec(compile(open(
#     os.path.join(
#       os.path.dirname(os.path.abspath(__file__)),
#       'taz',
#       '_version.py')).read(), 'fbd_tools/_version.py', 'exec'))


setup(name='cfa-taz',  # name your package
      packages=find_packages(exclude=['tests/config.py']),
      version=__version__,
      description='Hight level API for azure',
      long_description=long_description,
      package_dir={'taz': 'taz'},
      author='Christophe Fauchard',
      author_email='christophe.fauchard@gmail.com',
      license='MIT',  # MIT, GPL, BSD ??
      install_requires=[
          'azure-cli',
          'nose',
	  'pandas'
      ],
)
