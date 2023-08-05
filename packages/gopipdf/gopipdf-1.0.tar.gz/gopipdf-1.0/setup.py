import setuptools
from pathlib import Path

# finds packages exluding the ones mentioned, as tests and data are not packages , only .py files in goppdf folder are our packages
setuptools.setup(name='gopipdf', version=1.0, long_description=Path("README.md").read_text(),
                 packages=setuptools.find_packages(exclude=['tests', 'data']))
# above line is self explanoratory
# we need to give diff keyword arguments that give info on name, version etc..
