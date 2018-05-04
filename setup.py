#!/usr/bin/env python3

"""Setup file for easy installation."""
from setuptools import setup, find_packages

setup(
    name='unrar_wrapper',
    version='1.0.0',
    py_modules=['unrar_wrapper'],
    description='Backwards compatibility between unar and unrar',
    long_description=open('README.md', 'r', encoding='utf-8').read(),

    url='https://github.com/openSUSE/unrar_wrapper',
    download_url='https://github.com/openSUSE/unrar_wrapper',

    author='Kristyna Streitova',
    author_email='kstreitova@suse.com',

    maintainer='Kristyna Streitova',
    maintainer_email='kstreitova@suse.com',

    license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: System :: Archiving',
    ],
    keywords='unar unrar',
    platforms=['Linux'],

    test_suite="tests",

    entry_points={
        'console_scripts': ['unrar_wrapper = unrar_wrapper:main']},
)
