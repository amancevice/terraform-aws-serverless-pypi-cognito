import base64
from unittest import mock

import botocore.exceptions

USERNAME = 'fizz'
PASSWORD = 'buzz'
CREDS = base64.b64encode(f'{USERNAME}:{PASSWORD}'.encode()).decode()

with mock.patch('boto3.client'):
    import index


def test_handler_authorized():
    index.COGNITO.initiate_auth.return_value = True
    event = {
        'authorizationToken': f'Basic {CREDS}',
        'user': USERNAME,
        'methodArn': '<arn>/<stage>/GET/simple/pip',
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
                    'Resource': [
                        '<arn>/<stage>/GET/*',
                        '<arn>/<stage>/HEAD/*',
                    ],
                },
            ],
        },
    }
    assert ret == exp


def test_handler_unauthorized():
    index.COGNITO.initiate_auth.side_effect = botocore.exceptions.ClientError(
        error_response={},
        operation_name='InitiateAuth',
    )
    event = {
        'user': USERNAME,
        'methodArn': '<arn>/<stage>/GET/simple/pip',
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
                    'Resource': [
                        '<arn>/<stage>/GET/*',
                        '<arn>/<stage>/HEAD/*',
                    ],
                },
            ],
        },
    }
    assert ret == exp
