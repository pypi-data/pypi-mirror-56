from ftw.slacker.slack_notifier import DEACTIVATE_SLACK_NOTIFICATION
from ftw.slacker.slack_notifier import STANDARD_SLACK_WEBHOOK
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig
import os


class FtwSlackerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.slacker
        xmlconfig.file('configure.zcml',
                       ftw.slacker,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # Actiavte notifications for testing
        os.environ[DEACTIVATE_SLACK_NOTIFICATION] = ''

        # Reset the webhook url. You have to set it explicitly in tests.
        os.environ[STANDARD_SLACK_WEBHOOK] = ''

FTW_SLACKER_FIXTURE = FtwSlackerLayer()
FTW_SLACKER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_SLACKER_FIXTURE,), name="ftw.slacker:Functional")
