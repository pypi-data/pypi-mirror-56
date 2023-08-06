ftw.slacker
===========

.. contents:: Table of Contents


Introduction
------------

The ``ftw.slacker`` is a Plone addon that provides an easy to use api to post messages into a Slack channel through Slack's webhooks api.

For more information about slack webhooks see Slack's documentation about `Incoming Webhooks`_

Installation
------------

Add the package as dependency to your setup.py:

.. code:: python

  setup(
        # ...
        install_requires=[
          'ftw.slacker',
        ])

or to your buildout configuration:

.. code:: ini

  [instance]
  eggs += ftw.slacker

and run buildout

.. code:: bash

  bin/buildout

Usage
-----

Setup Slack webhook
~~~~~~~~~~~~~~~~~~~

First of all, you need to setup a Slack webhook.

Read the Slack documentation about `Incoming Webhooks`_ and start
setting up your own webhock by follow the `incoming webhook integration <https://my.slack.com/services/new/incoming-webhook/>`_.

Post message to Slack
~~~~~~~~~~~~~~~~~~~~~

Just import the `notify_slack` api function and call it.

.. code:: python

  from ftw.slacker import notify_slack

  notify_slack('https://hooks.slack.com/services/xxx',
               text="my first post")

Done!

Configure the requests module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following properties are passed to the requests module:

- `webhook_url <http://docs.python-requests.org/en/master/user/quickstart/>`_
- `timeout <http://docs.python-requests.org/en/master/user/quickstart/#timeouts>`_
- `verify <http://docs.python-requests.org/en/master/user/advanced/#ssl-cert-verification>`_

That means, you can call the api-function with this parameteres to configure the request:

.. code:: python

  from ftw.slacker import notify_slack

  notify_slack(webhook_url='https://hooks.slack.com/services/xxx',
               timemout=10,
               verify=False,
               text="my first post")

Slack payload
~~~~~~~~~~~~~

Just add additional keyword arguments to the api-function. All parameters will be passed
as payload to the Slack webhook.

.. code:: python

  from ftw.slacker import notify_slack

  notify_slack('https://hooks.slack.com/services/xxx',
               text="my first post",
               attachments=[
                   {
                       "title": "Slack API Documentation",
                       "title_link": "https://api.slack.com/",
                       "text": "Optional text that appears within the attachment"
                   }
               ])

Webhook URL by environment variables
------------------------------------

Normally you don't want to store your webhook-url in your application code.

``ftw.slacker`` supports configuration through environment-variables:

Set your environment variable:

.. code:: bash

  export STANDARD_SLACK_WEBHOOK='https://hooks.slack.com/services/xxx'

or through buildout:

.. code:: ini

  [instance]
  environment-vars +=
      STANDARD_SLACK_WEBHOOK https://hooks.slack.com/services/xxx

and call the api-function without webhook_url parameter:

.. code:: python

  from ftw.slacker import notify_slack

  notify_slack(text="my first post")

Override the environment variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you set the STANDARD_SLACK_WEBHOOK environment variable, you can still use a different
slack webhook.

.. code:: bash

  export STANDARD_SLACK_WEBHOOK='https://hooks.slack.com/services/default-channel-id'

.. code:: python

  from ftw.slacker import notify_slack

  # Post message to service default-channel-id
  notify_slack(text="my first post")

  # Post message to service specific-channel-id
  notify_slack('https://hooks.slack.com/services/specific-channel-id',
               text="my first post")

Deactivate Slack notification
-----------------------------

Let's imagine, you have a server with multiple deployments and all deployments should
push to the same Slack webhook.

You can either configure the standard slack webhook envoronment variable through buildout
for each deployment, or you just define the default webhook url once in your server environment:

.. code:: bash

  export STANDARD_SLACK_WEBHOOK='https://hooks.slack.com/services/xxx'

Each application will post messages to this slack webhook.

Blacklist
~~~~~~~~~

Now you install a test-deployment on the same server where you want to deactivate the notifications.

For this purpose, you can set another environment variable in this specific deployment's ``builodut.cfg`` to
the value: ``deactivate``. (see the static variable ``NOTIFICATION_DEACTIVATION_VALUE``):

.. code:: ini

  [instance]
  environment-vars +=
      DEACTIVATE_SLACK_NOTIFICATION deactivate

All notifications performed by this deployment will be skipped.

Whitelist
~~~~~~~~~

You could even do a whitelist for your deployments.

.. code:: bash

  export STANDARD_SLACK_WEBHOOK='https://hooks.slack.com/services/xxx'
  export DEACTIVATE_SLACK_NOTIFICATION deactivate

And for all whitelisted deployments, use the following buildout configuration:

.. code:: ini

  [instance]
  environment-vars +=
      DEACTIVATE_SLACK_NOTIFICATION

This will reset the DEACTIVATE_SLACK_NOTIFICATION variable to ``''``

Deactivate through webhook_url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's also possible to deactivate just a specific notification.

Let's say, you have set your STANDARD_SLACK_WEBHOOK. We've learned, that
you can call ``notify_slack`` without any webhook_url to push notification
to the standard webhook url or you can call it with a more specific webhook url
``notify_slack(webhook_url="xxx")`` to override the standard slack webhook.

Using the NOTIFICATION_DEACTIVATION_VALUE as the webhook_url will just deactivate
the current notification and will not bubble up to the standard slack webhook.

This feature is expecially useful for handling notification comming from multiple
external modules using the slacker-integration.

See the next chapter for more information about advanced usage.

Advance usage
-------------

Perhaps you've got different external modules using the ``ftw.slacker`` implementation and
all of this modules providing a different default slack webhook url.

Let's imagine, we have a module calling ``ftw.logger`` which logs all userlogins within your
plonesite to a slack-channel.

It provides an additional environment variable called ``FTW_LOGGER_SLACK_WEBHOOK`` to post the
logging-activities to a separate channel. So the implementation of this module may
look like this:

.. code:: python

  from ftw.slacker import notify_slack
  import os

  def notify_user_login(user):
      notify_slack(os.environ.get('FTW_LOGGER_SLACK_WEBHOOK'),
                   text='User {} logged in'.format(user.username))

If you don't set the ``FTW_LOGGER_SLACK_WEBHOOK`` variable, ``ftw.slacker`` will post the user
login to the default channel. If you set `FTW_LOGGER_SLACK_WEBHOOK`, ``ftw.slacker`` will
use this more specific channel for notifications.

Deactivating the whole notification system through the DEACTIVATE_SLACK_NOTIFICATION
environment variable is not desired, because you still want to post other notifications,
i.e. from your application which uses the standard slack webhook url.

For this puropose, you can just deactivate this specific notification branch by setting
the environment variable ``FTW_LOGGER_SLACK_WEBHOOK`` to ``deactivate`` (see the static
variable ``NOTIFICATION_DEACTIVATION_VALUE``).

.. code:: ini

  [instance]
  environment-vars +=
      STANDARD_SLACK_WEBHOOK https://hooks.slack.com/services/xxx
      FTW_LOGGER_SLACK_WEBHOOK deactivate

Threading
---------

All requests to the Slack-API will be handled within its own threads.
All messages are sent in a separate thread so that it is non-blocking and does not
crash the application on an error.

The function ``notify_slack`` returns the thread-object for further thread handlings (i.e. in testing) or none.

Links
-----

- Main project repository: https://github.com/4teamwork/ftw.slacker
- Issue tracker: https://github.com/4teamwork/ftw.slacker/issues

Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.slacker`` is licensed under GNU General Public License, version 2.

.. _Incoming Webhooks: https://api.slack.com/incoming-webhooks
