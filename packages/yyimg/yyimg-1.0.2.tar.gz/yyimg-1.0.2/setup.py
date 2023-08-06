from __future__ import print_function
from setuptools import setup
exec(open('yyimg/version.py').read())
print("Version NO:", __version__)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'yyimg',
    packages = ['yyimg'],
    version = __version__,
    description = 'image tools for deep learning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'YunYang1994',
    author_email = 'dreameryangyun@sjtu.edu.cn',
    url = 'https://github.com/YunYang1994/yyimg.git',
    keywords = ['deep-learning', 'image'], # arbitrary keywords
    classifiers = [],
)

