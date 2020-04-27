import base64
import json
import os

import boto3
import botocore

COGNITO = boto3.client('cognito-idp')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')


def handler(event, *_):
    """ Basic auth. """
    # Extract values from event
    print(f'EVENT {json.dumps(event)}')
    authorization_token = event.get('authorizationToken')
    user = event.get('user')
    method_arn = event.get('methodArn')
    arn, stage, _, *_ = method_arn.split('/')

    # Assemble response policy
    response = {
        'principalId': user,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Deny',
                    'Resource': [
                        f'{arn}/{stage}/GET/*',
                        f'{arn}/{stage}/HEAD/*',
                        f'{arn}/{stage}/POST/*',
                    ],
                },
            ],
        },
    }

    # Decode creds
    try:
        _, auth64 = authorization_token.split(' ')
        username, password = base64.b64decode(auth64).decode().split(':')
    except (AttributeError, ValueError):
        username = password = None

    try:
        auth = COGNITO.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=COGNITO_CLIENT_ID,
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            },
        )
    except botocore.exceptions.ClientError as err:
        print(err)
        auth = None

    # Update response
    if auth:
        [
            statement.update(Effect='Allow')
            for statement in response['policyDocument']['Statement']
        ]
    print(f'RESPONSE {response}')
    return response
