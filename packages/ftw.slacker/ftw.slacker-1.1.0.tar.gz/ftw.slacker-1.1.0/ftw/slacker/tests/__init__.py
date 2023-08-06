from contextlib import contextmanager
from ftw.slacker.testing import FTW_SLACKER_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest import TestCase
from ftw.slacker import slack_notifier
import transaction
import os
import sys


class FunctionalTestCase(TestCase):

    layer = FTW_SLACKER_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()

    def assertItemsEqual(self, actual, expected, msg=None):
        """Test that sequence expected contains the same elements as actual.
           regardless of their order.

           This method is renamed to assertCountEqual in Python 3.
        """
        if sys.version_info > (3, 0):
            return self.assertCountEqual(actual, expected, msg)
        return super(FunctionalTestCase, self).assertItemsEqual(actual, expected, msg)


class ResponseStub(object):

    def raise_for_status(self):
        pass


class RequestsMock(object):

    def __init__(self):
        self.posts = []

    def post(self, url, **kwargs):
        kwargs['url'] = url
        self.posts.append(kwargs)
        return ResponseStub()

    @classmethod
    @contextmanager
    def installed(kls):
        original_requests = slack_notifier.requests
        mock_requests = slack_notifier.requests = kls()
        try:
            yield mock_requests
        finally:
            slack_notifier.requests = original_requests


class ActivateEnvVariables(object):
    def __init__(self, **kwargs):
        self.variables = kwargs

    def __enter__(self):
        for key, value in self.variables.items():
            os.environ[key] = value

    def __exit__(self, *args):
        for key in self.variables.keys():
            del os.environ[key]
