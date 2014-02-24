:title: Python Testing Tools
:author: Carl Meyer
:description: a presentation for ConFoo 2014
:keywords: presentation, python, testing, confoo

:skip-help: true
:data-transition-duration: 400


----

:id: title

Python Testing Tools
====================

|hcard|

----

:id: thistalk
:data-reveal: 1

This talk
---------

* py.test

* fixtures

* parametrized tests

* test marking & skipping

* WebTest

* tox

* mock & pretend

* coverage

----

:data-reveal: 1

How
----

* Introduce a feature

* Example(s)

* Just a taste!

* Link to docs

* Python 3

.. note::

   Docs links on final slide. No stress; doc links will be live in online
   slides.

   All code is Py3, but will note Py2 differences.

----

:data-reveal: 1

Me
----

* Writing Python since 2002.

* Professionally since 2007.

* Mostly web development.

* OSS: pip, virtualenv, Django

----

py.test
=======

grades.py
---------

.. code:: python

   def get_level(min_grade, max_grade):
       if max_grade <= 6:
           return 'elementary'
       if min_grade > 6:
           return 'secondary'
       return None

.. invisible-code-block: python

   import sys, types
   sys.modules['grades'] = types.ModuleType('grades')
   sys.modules['grades'].get_level = get_level

test_grades.py
--------------

.. code:: python

   import grades

   def test_get_level():
       assert grades.get_level(2, 5) == 'elementary'


.. note::

   py.test will find and run tests in any file whose name begins with
   "test\_". Test functions also need to have names beginning with "test\_".

   Matching up "grades.py" with "test_grades.py" is not necessary, though often
   helpful to keep tests organized.

   (These naming conventions are customizable.)

----

::

   $ pip install pytest

::

   $ py.test
   ============== test session starts ========================
   platform linux -- Python 3.3.2 -- py-1.4.20 -- pytest-2.5.2
   collected 1 items

   test_grades.py .

   ============== 1 passed in 0.01 seconds ===================

.. note::

   To run the tests, just "pip install pytest" and run "py.test" - it will
   automatically find and run your tests. Here it runs our one test, which
   passes!

----

:data-reveal: 1

Python test runners
===================

A brief synopsis and digression
-------------------------------

* We saw `py.test`_ in action: ``pip install pytest; py.test``

  .. _py.test: http://pytest.org

* `Nose`_ is similar: ``pip install nose; nosetests``

  .. _Nose: https://nose.readthedocs.org/

* Both can run simple function tests with asserts.

* `unittest`_ is in the standard library, similar to "xUnit" test frameworks in
  various languages. Tests require a bit more boilerplate. ``python -m unittest
  discover``

  .. _unittest: http://docs.python.org/3.3/library/unittest.html

* Others: `twisted.trial`_, `zope.testrunner`_

  .. _twisted.trial: http://twistedmatrix.com/trac/wiki/TwistedTrial
  .. _zope.testrunner: https://pypi.python.org/pypi/zope.testrunner

.. note::

   If all these choices are overwhelming, don't worry about it. They're all
   fine, just pick one and run with it.

   My choice is py.test, so that's what I'll be covering today.


----

:data-reveal: 1

Choosing tests to run
---------------------

* Name a test file: ``py.test path/to/test_grades.py``

* Name a directory: ``py.test some/tests/``

* Match a keyword in test function name: ``py.test -k grades``

----

:id: questions

Questions?
==========

* `oddbird.net/python-testing-tools-preso`_

.. _oddbird.net/python-testing-tools-preso: http://oddbird.net/python-testing-tools-preso

|hcard|

.. |hcard| raw:: html

   <div class="vcard">
   <a href="http://www.oddbird.net">
     <img src="images/logo.svg" alt="OddBird" class="logo" />
   </a>
   <h2 class="fn">Carl Meyer</h2>
   <ul class="links">
     <li><a href="http://www.oddbird.net" class="org url">oddbird.net</a></li>
     <li><a href="https://twitter.com/carljm" rel="me">@carljm</a></li>
   </ul>
   </div>
