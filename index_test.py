import base64
import os
from unittest import mock

USERNAME = 'fizz'
PASSWORD = 'buzz'
CREDS = base64.b64encode(f'{USERNAME}:{PASSWORD}'.encode()).decode()
os.environ['BASIC_AUTH_USERNAME'] = 'fizz'
os.environ['BASIC_AUTH_PASSWORD'] = 'buzz'

with mock.patch('boto3.client'):
    import index


def test_handler_authorized():
    event = {
        'authorizationToken': f'Basic {CREDS}',
        'user': USERNAME,
        'methodArn': '<method-arn>',
    }
    ret = index.handler(event)
    exp = {
        'principalId': USERNAME,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Allow',
                    'Resource': '<method-arn>',
                },
            ],
        },
    }
    assert ret == exp


def test_handler_unauthorized():
    event = {
        'user': USERNAME,
        'methodArn': '<method-arn>',
    }
    ret = index.handler(event)
    exp = {
        'principalId': USERNAME,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Deny',
                    'Resource': '<method-arn>',
                },
            ],
        },
    }
    assert ret == exp
