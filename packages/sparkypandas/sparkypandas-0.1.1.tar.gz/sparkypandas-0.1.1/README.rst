===========
sparkypanda
===========


.. image:: https://img.shields.io/pypi/v/sparkypandas.svg
        :target: https://pypi.python.org/pypi/sparkypandas

.. image:: https://travis-ci.org/priamai/sparky-panda.svg?branch=master
    :target: https://travis-ci.org/priamai/sparky-panda

.. image:: https://readthedocs.org/projects/sparkypanda/badge/?version=latest
        :target: https://sparkypanda.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/priamai/sparky-panda/shield.svg
     :target: https://pyup.io/account/repos/github/priamai/sparky-panda
     :alt: Updates


A spark like interface to pandas data frames


* Free software: Apache Software License 2.0
* Documentation: https://sparkypanda.readthedocs.io.


Features
--------

* Implemented select expression

Example
------------------

First install:
pip install sparkypandas


.. code-block:: python

    import sparypanda
    data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}

    df = sparkypanda.DataFrame(data)

    df_all_col = df.select('*')

    df_col_1 = df.select('col_1')

    df_all = df.select('col_2','col_1')


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
