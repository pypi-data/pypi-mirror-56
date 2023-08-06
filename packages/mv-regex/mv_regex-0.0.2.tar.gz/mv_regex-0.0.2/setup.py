
from setuptools import setup
import re

filepath = 'mv_regex/__init__.py'
__version__ = re.findall(r'__version__ = \'(.*)\'', open(filepath).read())[0]

setup(
    name = 'mv_regex',
    version = __version__,
    license = 'MIT',
    author = 'Tom de Geus',
    author_email = 'tom@geus.me',
    description = 'Move files by applying an regular expression',
    long_description = 'Move files by applying an regular expression',
    keywords = 'regex',
    url = 'https://github.com/tdegeus/mv_regex',
    packages = ['mv_regex'],
    install_requires = ['docopt>=0.6.2', 'click>=4.0'],
    entry_points = {
        'console_scripts': ['mv_regex = mv_regex:main']})
