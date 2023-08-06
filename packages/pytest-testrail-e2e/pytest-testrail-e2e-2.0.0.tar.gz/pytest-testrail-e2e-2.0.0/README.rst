pytest-testrail-e2e
===================

|PyPI version| |License|

This is a pytest plugin for creating/editing testplans or testruns based
on pytest markers. The results of the collected tests will be updated
against the testplan/testrun in TestRail.

Installation
------------

::

   pip install pytest-testrail-e2e

Configuration
-------------

Config for Pytest tests
~~~~~~~~~~~~~~~~~~~~~~~

Add a marker to the tests that will be picked up to be added to the run.

.. code:: python

   from pytest_testrail.plugin import testrail

   @testrail('C1234', 'C5678')
   def test_foo():
       # test code goes here

   # OR    

   from pytest_testrail.plugin import pytestrail

   @pytestrail.case('C1234', 'C5678')
   def test_bar():
       # test code goes here

Config for TestRail
~~~~~~~~~~~~~~~~~~~

-  Settings file template config:

.. code:: ini

   [API]
   url = https://yoururl.testrail.net/
   email = user@email.com
   password = <api_key>

   [TESTRUN]
   assignedto_id = 1
   project_id = 2
   suite_id = 3

Or

-  Set command line options (see below)

Usage
-----

Basically, the following command will create a testrun in TestRail, add
all marked tests to run. Once the all tests are finished they will be
updated in TestRail:

.. code:: bash

   py.test --testrail --tr-config=<settings file>.cfg

All available options
~~~~~~~~~~~~~~~~~~~~~

::

     --testrail            Create and update testruns with TestRail
     --tr-config=TR_CONFIG
                           Path to the config file containing information about
                           the TestRail server (defaults to testrail.cfg)
     --tr-url=TR_URL       TestRail address you use to access TestRail with your
                           web browser (config file: url in API section)
     --tr-email=TR_EMAIL   Email for the account on the TestRail server (config
                           file: email in API section)
     --tr-password=TR_PASSWORD
                           Password for the account on the TestRail server
                           (config file: password in API section)
     --tr-testrun-assignedto-id=TR_TESTRUN_ASSIGNEDTO_ID
                           ID of the user assigned to the test run (config file:
                           assignedto_id in TESTRUN section)
     --tr-testrun-project-id=TR_TESTRUN_PROJECT_ID
                           ID of the project the test run is in (config file:
                           project_id in TESTRUN section)
     --tr-testrun-suite-id=TR_TESTRUN_SUITE_ID
                           ID of the test suite containing the test cases (config
                           file: suite_id in TESTRUN section)
     --tr-testrun-suite-include-all
                           Include all test cases in specified test suite when
                           creating test run (config file: include_all in TESTRUN
                           section)
     --tr-testrun-name=TR_TESTRUN_NAME
                           Name given to testrun, that appears in TestRail
                           (config file: name in TESTRUN section)
     --tr-run-id=TR_RUN_ID
                           Identifier of testrun, that appears in TestRail. If
                           provided, option "--tr-testrun-name" will be ignored
     --tr-plan-id=TR_PLAN_ID
                           Identifier of testplan, that appears in TestRail. If
                           provided, option "--tr-testrun-name" will be ignored
     --tr-version=TR_VERSION
                           Indicate a version in Test Case result.
     --tr-no-ssl-cert-check
                           Do not check for valid SSL certificate on TestRail
                           host
     --tr-close-on-complete
                           Close a test plan or test run on completion.
     --tr-dont-publish-blocked
                           Do not publish results of "blocked" testcases in
                           TestRail
     --tr-skip-missing     Skip test cases that are not present in testrun
     --tr-report-single-test
                           Report result immediately for each test case when it finished

.. |PyPI version| image:: https://badge.fury.io/py/pytest-testrail-e2e.svg
   :target: https://badge.fury.io/py/pytest-testrail-e2e
.. |License| image:: http://img.shields.io/badge/license-MIT-brightgreen.svg
   :target: https://github.com/vietnq254/pytest-testrail-e2e/blob/master/LICENSE

TestRail Settings
=================

To increase security, the TestRail team suggests using an API key instead of a password. You can see how to generate an API key `here <http://docs.gurock.com/testrail-api2/accessing#username_and_api_key>`__.

If you maintain your own TestRail instance on your own server, it is recommended to `enable HTTPS for your TestRail installation <http://docs.gurock.com/testrail-admin/admin-securing#using_https>`__.

For TestRail hosted accounts maintained by `Gurock <http://www.gurock.com/>`__, all accounts will automatically use HTTPS.

You can read the whole TestRail documentation `here <http://docs.gurock.com/>`__.

Author
======

NGUYEN Viet - `github <https://github.com/vietnq254>`__.

License
=======

This project is licensed under the `MIT license <https://github.com/vietnq254/pytest-testrail-e2e/blob/master/LICENSE>`__.

Acknowledgments
===============

* `allankp <https://github.com/allankp>`__, author of the `pytest-testrail <https://github.com/allankp/pytest-testrail>`__ repository that was cloned.