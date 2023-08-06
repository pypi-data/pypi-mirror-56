#!/usr/bin/env python3

# Copyright 2019 Marcos Del Sol Vives <marcos@orca.pet>
# SPDX-License-Identifier: WTFPL

import os.path
from setuptools import setup, find_packages

def read(file):
	this_directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(this_directory, file), encoding='utf-8') as f:
		content = f.read()
	return content

setup(
	name='saph',
	packages=['saph'],
	version='1.0',
	install_requires=[
		# PyCryptodrome, at least the first version having "output" parameter in .encrypt()
		'pycryptodome>=3.7.0',
	],

	license='WTFPL',
	description='Stupid Algorithm for Password Hashing',
	long_description=read('README.md'),
	long_description_content_type='text/markdown',

	keywords='password hashing hash passphrase storage',
	classifiers=[
		'Topic :: Security',
		'Topic :: Security :: Cryptography',
		'License :: Freely Distributable'
	],

	url='https://github.com/socram8888/saph-python',
	project_urls={
		'Bug Tracker': 'https://github.com/socram8888/saph-python/issues',
		'Source Code': 'https://github.com/socram8888/saph-python'
	},

	author='Marcos Del Sol Vives',
	author_email='marcos@orca.pet',
)
