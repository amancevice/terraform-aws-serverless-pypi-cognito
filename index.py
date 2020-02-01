import base64
import json
import os

BASIC_AUTH_USERNAME = os.getenv('BASIC_AUTH_USERNAME')
BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD')


def handler(event, *_):
    """ Basic auth. """
    # Extract values from event
    print(f'EVENT {json.dumps(event)}')
    authorization_token = event.get('authorizationToken')
    user = event.get('user')
    method_arn = event.get('methodArn')

    # Assemble response policy
    response = {
        'principalId': user,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Deny',
                    'Resource': method_arn,
                },
            ],
        },
    }

    # Decode creds
    try:
        _, auth64 = authorization_token.split(' ')
        username, password = base64.b64decode(auth64).decode().split(':')
    except AttributeError:
        username = password = None

    # Update response
    user_ok = BASIC_AUTH_USERNAME == username
    pass_ok = BASIC_AUTH_PASSWORD == password
    if user_ok and pass_ok:
        [
            statement.update(Effect='Allow')
            for statement in response['policyDocument']['Statement']
        ]
    print(f'RESPONSE {response}')
    return response
