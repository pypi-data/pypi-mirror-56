=====================================
Cool Django Authentication Using LDAP
=====================================

.. include:: badges-doc.rst

This is a Django authentication backend that authenticates against an LDAP
service. Configuration can be as simple as a single distinguished name
template, but there are many rich configuration options for working with users,
groups, and permissions.

This version is supported on Python 3.5+; and Django 1.11+. It requires
`python-ldap`_ >= 3.1.

.. toctree::
    :maxdepth: 2

    install
    authentication
    groups
    users
    permissions
    multiconfig
    custombehavior
    logging
    performance
    example
    reference
    changes
    contributing

.. _`python-ldap`: https://pypi.org/project/python-ldap/


License
=======

.. include:: ../LICENSE
