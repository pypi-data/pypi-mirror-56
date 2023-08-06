#!/usr/bin/env python
# coding: utf-8
from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = ""

setup(
	name="datamining",
	version="0.1.2",
	author="kxy",
	author_email="907250734@qq.com",
	description="data mining code",
	long_description=long_description,
	url="https://github.com/770120041/DataMiningWebsite",
	packages=['datamining'],
	install_requires=[
	],
	classifiers=[
		"Environment :: Web Environment",
		"Intended Audience :: Developers",
		"Operating System :: OS Independent",
		"Topic :: Text Processing :: Indexing",
		"Topic :: Utilities",
		"Topic :: Internet",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7'
	],
)