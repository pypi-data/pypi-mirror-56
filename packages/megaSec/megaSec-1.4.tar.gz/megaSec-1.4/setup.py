# -*- coding: utf-8 -*-

from setuptools import setup

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft',
    'Programming Language :: Python :: 3.7',
    'Topic :: Internet :: Proxy Servers',

]

setup(
    name = 'megaSec',
    packages = ['megaAPI'],
    scripts = [],
    version = '1.4',
    description = 'MegaSec API',
    author = 'TZHAN',    
    url = 'https://github.com/cloud3940/megaSec',    
    license = 'MIT',
    keywords = ['mega'],
    classifiers = classifiers,
    package_data={  # Optional
        'megaAPI': ['uFIISAPI.dll', 'uFIISAPI.lib','mobapips.dll'],
    }
)