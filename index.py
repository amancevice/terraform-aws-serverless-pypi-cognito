import base64
import json
import os

BASIC_AUTH_USERNAME = os.getenv('BASIC_AUTH_USERNAME')
BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD')


def handler(event, *_):
    """ Basic auth. """
    print(f'EVENT {json.dumps(event)}')
    _, auth64 = event['authorizationToken'].split(' ')
    username, password = base64.b64decode(auth64).decode().split(':')
    print(f'USERNAME {username}')
    print(f'PASSWORD {password}')
    response = {
        'principalId': event.get('user'),
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Deny',
                    'Resource': event.get('methodArn'),
                },
            ],
        },
    }
    user_ok = BASIC_AUTH_USERNAME == username
    pass_ok = BASIC_AUTH_PASSWORD == password
    if user_ok and pass_ok:
        [
            statement.update(Effect='Allow')
            for statement in response['policyDocument']['Statement']
        ]
    print(f'RESPONSE {response}')
    return response
