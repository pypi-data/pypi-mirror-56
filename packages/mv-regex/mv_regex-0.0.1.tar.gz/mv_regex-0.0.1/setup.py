
from setuptools import setup

setup(
    name = 'mv_regex',
    version = '0.0.1',
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
