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

* test marking & skipping

* fixtures

* parametrized tests

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
   "test\_". Test functions also need to have names beginning with "test".

   Matching up "grades.py" with "test_grades.py" is not necessary, though often
   helpful to keep tests organized.

   (These naming conventions are customizable.)

----

:data-emphasize-lines-step: 1,2,4,5,7,9

.. code::
   :number-lines:

   $ pip install pytest

.. code::
   :number-lines:

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

* Match test function/class name: ``py.test -k grades``

* Select tests by "mark": ``py.test -m "not slow"``

.. note::

   Flexible matching of tests to run - very important for fast edit/test
   cycles, especially in larger projects.

   Select by mark - which raises the question...

----

:data-emphasize-lines-step: 3
:data-reveal: 1

Wait, what's a "mark"?
----------------------

.. code:: python
   :number-lines:

   import pytest

   @pytest.mark.slow
   def test_something_very_slow():
       """Can download the internet."""
       # ...

* ``py.test -m slow`` will run only tests with this mark.

* ``py.test -m "not slow"`` will run only tests without it.

* Can also use ``and`` / ``or`` for conditions with multiple marks.

.. note::

   You can use any mark names you want (valid Python identifiers) or configure
   a restricted set for the project in your ``pytest.ini`` file.

----

:data-emphasize-lines-step: 2,3,4,5,6,7,8,9

pytest.ini
----------

.. code:: ini
   :number-lines:

   [pytest]
   minversion = 2.4.2
   addopts = --strict --cov-report html --cov myproj
   norecursedirs = .* _* selenium node_modules qunit
   python_files = test_*.py
   python_classes = Test
   python_functions = test
   markers =
       slow: mark a test as slow
       web: mark a test as a web test

.. note::

   All optional.

   If you use markers, recommended to list valid markers so there's one
   reference point for all markers used, and typos become errors (with
   ``strict``). At some point in the future pytest may require markers to be
   registered.

----

:data-reveal: 1

Classes?
--------

.. code:: python

   class TestPager:
       def test_num_pages(self):
           """Can calculate total number of pages."""
           assert pager(count=23, pagesize=10).num_pages == 3

       def test_item_range(self):
           """Can calculate range of items to be shown."""
           # ...

* Can use classes to group related tests, but not required.

* Unlike ``unittest``, no special ``TestCase`` class to inherit from.

* Avoid using classes for setup/teardown (use fixtures).

* Avoid using classes to parametrize tests (use parametrized tests).

----

:data-emphasize-lines-step: 4,5

Test skipping
=============

Not all tests can run in all environments.
------------------------------------------

.. code:: python
   :number-lines:

   import sys
   import pytest

   @pytest.mark.skipif(
       sys.platform != 'win32', reason='Windows specific')
   def test_updates_registry():
       """Checks and updates registry entries."""
       # ...

.. note::

   Can mark any test to be skipped under some conditions.

----

:data-emphasize-lines-step: 6,9,16

.. code::
   :number-lines:

   $ py.test
   ================ test session starts ======================
   platform linux -- Python 3.3.2 -- py-1.4.20 -- pytest-2.5.2
   collected 4 items

   test_grades.py ...s

   ================ 3 passed, 1 skipped in 0.02 seconds ======

.. code::
   :number-lines:

   $ py.test -rs
   ================ test session starts ======================
   platform linux -- Python 3.3.2 -- py-1.4.20 -- pytest-2.5.2
   collected 4 items

   test_grades.py ...s
   ================ short test summary info ==================
   SKIP [1] /.../_pytest/skipping.py:132: Windows specific

   ================ 3 passed, 1 skipped in 0.02 seconds ======

.. note::

   Skipped tests show up as an 's' instead of a '.'.

   Run py.test with '-rs' to show reasons for skipped tests.

----

:data-emphasize-lines-step: 4,5
:data-reveal: 1

Expected failures
=================

Sometimes we expect a test to fail, for now.
--------------------------------------------

.. code:: python
   :number-lines:

   import sys
   import pytest

   @pytest.mark.xfail(
       sys.version_info >= (3, 4), reason="Buggy on Py 3.4")
   def test_something_that_doesnt_work_yet_on_python_34():
       pass # ...

* Just like ``-rs`` for skips, ``-rx`` will provide additional info on expected
  failures.

* ``xfail`` tests will report an ``X`` (``xpass`` or "unexpected pass") if they
  pass.

* Use ``--runxfail`` to run ``xfail`` tests normally (report failures as
  failures).

.. note::

   May be a low priority bug that we plan to fix, or a feature we haven't fully
   implemented yet.

   Can also unconditionally xfail, provide only a reason.

----

:id: questions

Questions?
==========

* `oddbird.net/python-testing-tools-preso`_
* `pytest.org`_

.. _oddbird.net/python-testing-tools-preso: http://oddbird.net/python-testing-tools-preso
.. _pytest.org: http://pytest.org

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
