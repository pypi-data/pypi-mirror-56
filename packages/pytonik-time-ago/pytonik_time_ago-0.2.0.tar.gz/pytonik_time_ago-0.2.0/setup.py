# Author : BetaCodings
# Author : info@betacodings.com
# Maintainer By: Emmanuel Martins
# Maintainer Email: emmamartinscm@gmail.com
# Created by BetaCodings on 18/11/2019.
import sys

VERSION = (0, 2, 0, '', 1)

if VERSION[3] and VERSION[4]:
	VERSION_TEXT = '{0}.{1}.{2}{3}{4}'.format(*VERSION)
else:
	VERSION_TEXT = '{0}.{1}.{2}'.format(*VERSION[0:3])

VERSION_EXTRA = ''
LICENSE = 'Apache 2.0'#MIT
EDITION = ''  # Added in package names, after the version
KEYWORDS = "mvc, oop, module, framework, pytonik, time, date, timeago, readable time"

PYVERSION_MA = sys.version_info.major
PYVERSION_MI = sys.version_info.minor


from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fd:
    longdescription = fd.read()



setup(
    name='pytonik_time_ago',
    version = VERSION_TEXT,
    description='pytonik date and time ago readable format',
    url="https://github.com/pytonik/pytonik_time_ago",
    author='pytonik',
    author_email='info@pytonik.com',
    maintainer= 'Emmanuel Essien',
    maintainer_email='emmamartinscm@gmail.com',
    packages=find_namespace_packages(include=['*', '']),
    long_description = longdescription,
    long_description_content_type='text/markdown',
    license= LICENSE,
    keywords = KEYWORDS,
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python',
        'Topic :: Office/Business',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python'
    ],
    python_requires='>=2.7, >=3',
)
