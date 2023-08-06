import os
from setuptools import setup
#from distutils.core import setup

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='lab2blog',
    version='0.1',
    packages=['lab2blog'],

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    # url='http://yeisoncardona.com/',
    download_url='https://bitbucket.org/yeisoneng/lab2blog/downloads/',

    install_requires=[
    ],

    scripts=[
        "cmd/lab2blog",
    ],

    # zip_safe=False,

    include_package_data=True,
    license='BSD License',
    description="Jupyter Lab to HTML",
    #    long_description = README,

    classifiers=[

    ],

)
