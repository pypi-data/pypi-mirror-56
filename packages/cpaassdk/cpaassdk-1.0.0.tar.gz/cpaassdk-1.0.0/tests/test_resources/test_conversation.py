import responses

from cpaassdk.resources.conversation import Conversation, NotificationChannel
from tests.util import decallmethods, deep_equal
from tests.mocker import mock

@decallmethods(responses.activate)
class TestConversation:
  def base_url(self, api):
    return '/cpaas/smsmessaging/v1/{}'.format(api.user_id)

  def noitifcation_channel_base_url(self, api):
    return '/cpaas/notificationchannel/v1/{}'.format(api.user_id)

  def client(self, api):
    return Conversation(api)

  def test_send(self, api):
    client = Conversation(api)
    sender_address = '123'
    url = '{}/outbound/{}/requests'.format(self.base_url(api), sender_address)
    params = {
      'type': 'sms',
      'sender_address': sender_address,
      'destination_address': [ '345', '567' ],
      'message': 'Test message'
    }

    expected_body = {
      'outboundSMSMessageRequest': {
        'address': [ '345', '567' ],
        'clientCorrelator': 'test-client-id-python',
        'outboundSMSTextMessage': {
          'message': 'Test message'
        }
      }
    }

    mock(url, 'POST')

    response = client.create_message(params)

    assert response['__for_test__']['url'] == api.config.base_url + url
    assert deep_equal(response['__for_test__']['body'], expected_body)

  def test_delete(self, api):
    client = Conversation(api)
    remote_address = 'test-remote-address'
    local_address = 'test-local-address'
    url = '{}/remoteAddresses/{}/localAddresses/{}'.format(self.base_url(api), remote_address, local_address)
    params = {
      'type': 'sms',
      'remote_address': remote_address,
      'local_address': local_address
    }

    mock(url, 'DELETE')

    response = client.delete_message(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_delete_with_message_id(self, api):
    client = Conversation(api)
    remote_address = 'test-remote-address'
    local_address = 'test-local-address'
    message_id = 'test-message-id'
    url = '{}/remoteAddresses/{}/localAddresses/{}/messages/{}'.format(self.base_url(api), remote_address, local_address, message_id)
    params = {
      'type': 'sms',
      'remote_address': remote_address,
      'local_address': local_address,
      'message_id': message_id
    }

    mock(url, 'DELETE')

    response = client.delete_message(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_read_thread(self, api):
    client = Conversation(api)
    remote_address = 'test-remote-address'
    local_address = 'test-local-address'
    url = '{}/remoteAddresses/{}/localAddresses/{}/messages?max=10&new=test'.format(self.base_url(api), remote_address, local_address)
    params = {
      'type': 'sms',
      'remote_address': remote_address,
      'local_address': local_address,
      'query': {
        'max': 10,
        'new': 'test'
      }
    }

    mock(url, 'GET')

    response = client.get_messages_in_thread(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_status(self, api):
    client = Conversation(api)
    remote_address = 'test-remote-address'
    local_address = 'test-local-address'
    message_id = 'test-message-id'
    url = '{}/remoteAddresses/{}/localAddresses/{}/messages/{}/status'.format(self.base_url(api), remote_address, local_address, message_id)
    params = {
      'type': 'sms',
      'remote_address': remote_address,
      'local_address': local_address,
      'message_id': message_id
    }

    mock(url, 'GET')

    response = client.get_status(params)
    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_read_inbound_subscriptions(self, api):
    client = Conversation(api)
    url = '{}/inbound/subscriptions'.format(self.base_url(api))

    mock(url, 'GET')

    params = {
      'type': 'sms'
    }

    response = client.read_inbound_subscriptions(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_read_inbound_subscriptions(self, api):
    client = Conversation(api)
    subscription_id = 'test-subscription-id'
    url = '{}/inbound/subscriptions/{}'.format(self.base_url(api), subscription_id)
    params = {
      'type': 'sms',
      'subscription_id': subscription_id
    }

    mock(url, 'GET')

    response = client.get_subscription(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_create_inbound_subscription(self, api):
    # create_notification_channel
    client = NotificationChannel(api)
    url = '{}/channels'.format(self.noitifcation_channel_base_url(api))
    
    resp_body = {
      '__for_test__': {
        'channel_id': 'test-channel-id'
      },
      'channel_id': 'test-channel-id'
    }
    mock(url, 'POST', resp_body)

    params = {
      'webhook_url': 'test-webhook-url'
    }
    response = client.create_channel(params)
    
    client = Conversation(api)
    url = '{}/inbound/subscriptions'.format(self.base_url(api))
    params = {
      'type': 'sms',
      'webhook_url': 'test-webhook-url',
    }
    expected_body = {
      'subscription': {
        'callbackReference': {
          'notifyURL': 'test-notify-url'
        },
        'clientCorrelator': 'test-client-correlator'
      }
    }

    mock(url, 'POST')
    response = client.subscribe(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_create_inbound_subscription_with_all_params(self, api):
    # create_notification_channel
    client = NotificationChannel(api)
    url = '{}/channels'.format(self.noitifcation_channel_base_url(api))
    
    resp_body = {
      '__for_test__': {
        'channel_id': 'test-channel-id'
      },
      'channel_id': 'test-channel-id'
    }
    mock(url, 'POST', resp_body)

    params = {
      'webhook_url': 'test-webhook-url'
    }
    response = client.create_channel(params)

    client = Conversation(api)
    url = '{}/inbound/subscriptions'.format(self.base_url(api))
    params = {
      'type': 'sms',
      'webhook_url': 'test-webhook-url',
      'client_correlator': 'test-client-correlator',
      'destination_address': '123123'
    }
    expected_body = {
      'subscription': {
        'callbackReference': {
          'notifyURL': 'test-notify-url'
        },
        'clientCorrelator': 'test-client-correlator',
        'destinationAddress': '123123'
      }
    }

    mock(url, 'POST')

    response = client.subscribe(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_unsubscribe_inbound_subscription(self, api):
    client = Conversation(api)
    subscription_id = 'test-subscription-id'
    url = '{}/inbound/subscriptions/{}'.format(self.base_url(api), subscription_id)
    params = {
      'type': 'sms',
      'subscription_id': subscription_id
    }

    mock(url, 'DELETE')

    response = client.unsubscribe(params)

    assert response['__for_test__']['url'] == api.config.base_url + url
