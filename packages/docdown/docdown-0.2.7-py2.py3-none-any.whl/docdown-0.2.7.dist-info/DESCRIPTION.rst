===============================
Python DocDown
===============================

Python DocDown is a suite of extensions for `Python Markdown`_.

.. image:: https://travis-ci.org/livio/DocDown-Python.svg?branch=master
    :target: https://travis-ci.org/livio/DocDown-Python


Documentation
----------------

Run ``make docs`` to build the HTML documentation for Python DocDown

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Python Markdown`: https://pypi.python.org/pypi/Markdown


=======
History
=======

0.2.7 (2019-11-20)
------------------

* Fix case where '|||' in a table started a sequence diagram.

0.2.6 (2019-06-12)
------------------

* Fix block paragraph rendering with title

0.2.5 (2019-06-12)
------------------

* Fix whitespace issues with back to back tags

0.2.4 (2019-06-11)
------------------

* Fix whitespace issues with inline platform tags breaking markdown table formatting

0.2.3 (2019-06-06)
------------------

* Add support for inline platform section tags

0.2.2 (2019-06-05)
------------------

* Fix Platform Section Markdown Extension bug with spaces in platform section names

0.2.1 (2019-05-31)
------------------

* Fix Platform Section Markdown Extension bug with code blocks

0.2.0 (2019-05-29)
------------------

* Add Platform Section Markdown Extension


0.1.2 (2016-12-16)
------------------

* Strip leading ./ from media urls when concatenating with a set media_url
  in media and sequence diagram extensions.


0.1.1 (2016-12-15)
------------------

* Fix the distribution so that template_adapters work

0.1.0 (2016-12-13)
------------------

* First release on PyPI.


