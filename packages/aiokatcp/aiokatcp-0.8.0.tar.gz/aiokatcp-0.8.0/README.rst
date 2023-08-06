aiokatcp
========

.. image:: https://travis-ci.org/ska-sa/aiokatcp.svg?branch=master
   :target: https://travis-ci.org/ska-sa/aiokatcp
.. image:: https://coveralls.io/repos/github/ska-sa/aiokatcp/badge.svg
   :target: https://coveralls.io/github/ska-sa/aiokatcp
.. image:: https://readthedocs.org/projects/aiokatcp/badge/?version=latest
   :target: http://aiokatcp.readthedocs.io/en/latest/

aiokatcp is an implementation of the `katcp`_ protocol based around the Python
asyncio system module. It requires Python 3.5 or later, as it makes extensive
uses of coroutines and type annotations. It is loosely inspired by the `Python
2 bindings`_, but has a much narrower scope.

.. _katcp: https://katcp-python.readthedocs.io/en/latest/_downloads/NRF-KAT7-6.0-IFCE-002-Rev5.pdf

.. _Python 2 bindings: https://github.com/ska-sa/katcp-python

The current implementation provides both client and server APIs. It only
supports katcp version 5, and does not support a number of features that are
marked deprecated in version 5.

Full documentation can be found on `readthedocs`_.

.. _readthedocs: http://aiokatcp.readthedocs.io/en/latest/
