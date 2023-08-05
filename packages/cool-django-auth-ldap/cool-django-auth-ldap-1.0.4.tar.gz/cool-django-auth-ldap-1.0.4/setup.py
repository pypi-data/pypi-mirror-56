#!/usr/bin/env python

from setuptools import setup

import cool_django_auth_ldap

with open("README.rst") as fp:
    readme = fp.read()

setup(
    setup_requires=['pbr'],
    pbr=True
)
