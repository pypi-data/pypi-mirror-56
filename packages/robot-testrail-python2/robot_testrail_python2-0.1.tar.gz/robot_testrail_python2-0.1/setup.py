# To use a consistent encoding
from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='robot_testrail_python2',
    packages=['robot_testrail_python2'],
    version='0.1',
    license='Apache-2.0',
    description='Integration Robot Framework with TestRail for python 2.7',
    author='Maria Shyrko',
    author_email='shirko_2000@yahoo.com',
    url='https://github.com/MariaLviv/robot_testrail_python2',
    keywords=['testing', 'testautomation', 'robotframework', 'testrail', 'robot'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Framework :: Robot Framework :: Library',
    ],
)

