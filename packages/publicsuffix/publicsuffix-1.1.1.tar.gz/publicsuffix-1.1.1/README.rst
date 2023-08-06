Public Suffix List module for Python
====================================

Deprecated
----------

Please don't use this module. It is provided for historical reasons only. New
code should instead use one of the other libraries that provide similar
functionality. For example:

 * publicsuffix2_
 * publicsuffixlist_

.. _publicsuffix2: https://pypi.org/project/publicsuffix2
.. _publicsuffixlist: https://pypi.org/project/publicsuffixlist

About
-----

This module allows you to get the public suffix of a domain name using the
Public Suffix List from http://publicsuffix.org

A public suffix is one under which Internet users can directly register
names. Some examples of public suffixes are .com, .co.uk and pvt.k12.wy.us.
Accurately knowing the public suffix of a domain is useful when handling
web browser cookies, highlighting the most important part of a domain name
in a user interface or sorting URLs by web site.

It's up the user to provide this module with an appropriate version of the
Public Suffix List. A convenience function is provided that downloads the most
recent version available on http://publicsuffix.org


Module content
--------------

The `fetch()` function downloads the most recent version of the list and
returns a file object. You should cache the data as appropriate for your
application::

    >>> from publicsuffix import fetch
    >>> psl_file = fetch()

Alternatively, if you have the list already downloaded by other means::

    >>> import codecs
    >>> psl_file = codecs.open('publicsuffix/public_suffix_list.dat', encoding='utf8')

The `PublicSuffixList` class parses the Public Suffix List and allows queries
for individual domain names::

    >>> from publicsuffix import PublicSuffixList
    >>> psl = PublicSuffixList(psl_file)
    >>> psl.get_public_suffix("www.example.com")
    'example.com'

Please note that the ``host`` part of an URL can contain strings that are
not plain DNS domain names (IP addresses, Punycode-encoded names, name in
combination with a port number or an username, etc.). It is up to the
caller to ensure only domain names are passed to the get_public_suffix()
method.



Installation
------------

To install from the source distribution and run unit tests, use these
commands::

    $ python setup.py install
    $ python setup.py test


Source
------

You can get a local copy of the development repository with::

    git clone https://www.tablix.org/~avian/git/publicsuffix.git


Notes on backwards compatibility
--------------------------------

This module ships with an out-dated copy of the Public Suffix List for
compatibility with older versions. Use of this list is deprecated since it
encouraged applications that never updated the Public Suffix List data. The
built-in list will be removed in a future version.

If you are using the `PublicSuffixList` constructor without any arguments,
please use the `fetch()` function and implement an appropriate cache, as shown
above.


Support
-------

See deprecation notice above. In case of major bugs affecting legacy software
that hasn't yet migrated to other libraries, contact `tomaz.solc@tablix.org`.

..
    vim: set filetype=rst:
