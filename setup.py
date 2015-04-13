#!/usr/bin/python2.7

from setuptools import setup

setup(
    name             = 'questionnaire',
    version          = '1.0.0',
    author           = 'Benjamin David Holmes',
    author_email     = 'ben@bdholmes.com',
    url              = 'https://bitbucket.org/Aldarn/questionnaire',
    download_url     = 'https://bitbucket.org/Aldarn/questionnaire/downloads',
    description      = 'Simple MySQL driven command line questionnaire with per-question percentage chance of acceptance.',
    py_modules       = ['launch_questionnaire'],
    package_dir      = {'': 'src'},
    license          = 'GPLv3+',
    long_description = open( "readme.md" ).read(),
	install_requires = ['MySQL-python', 'fake-factory'],
	tests_require 	 = ['mock'],
    classifiers 	 = [
        'Environment :: Console',
		'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: Other/Nonlisted Topic',
		'Topic :: Scientific/Engineering :: Information Analysis'
    ]
) 