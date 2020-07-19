import base64
import json
import os

import boto3
import botocore

COGNITO = boto3.client('cognito-idp')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')


def handler(event, *_):
    """
    Basic auth.
    """
    # Extract values from event
    print(f'EVENT {json.dumps(event)}')
    authorization_token = event.get('authorizationToken')
    user = event.get('user')
    arn, stage, _, *_ = event.get('methodArn').split('/')

    # Decode creds
    username, password = decode_creds(authorization_token)

    # Attempt to authorize
    effect = get_effect(username, password)

    # Assemble response policy document
    response = get_policy_document(user, effect, arn, stage)

    # Send response
    print(f'RESPONSE {response}')
    return response


def decode_creds(authorization_token):
    """
    Decode Basic auth token into username, password.

    :param str authorization_token: Basic auth token
    :returns tuple: (username, password)
    """
    try:
        _, auth64 = authorization_token.split(' ')
        username, password = base64.b64decode(auth64).decode().split(':')
    except (AttributeError, ValueError):
        username = password = None
    return (username, password)


def get_effect(username, password):
    """
    Log in using Cognito USER_PASSWORD_AUTH flow.

    :param str username: Cognito username
    :param str password: Cognito password
    :returns str: {Allow,Deny}
    """
    try:
        COGNITO.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=COGNITO_CLIENT_ID,
            AuthParameters=dict(USERNAME=username, PASSWORD=password),
        )
        return 'Allow'
    except botocore.exceptions.ClientError as err:
        print(f'ERROR {err}')
        return 'Deny'


def get_policy_document(user, effect, arn, stage):
    """
    Get IAM policy for REST API resource access.

    :param str user: User initiating request
    :param str effect: {Allow,Deny}
    :param str arn: REST API resource ARN
    :param str stage: REST API stage name
    :returns dict: IAM policy document
    """
    return {
        'principalId': user,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': [
                        f'{arn}/{stage}/GET/*',
                        f'{arn}/{stage}/HEAD/*',
                        f'{arn}/{stage}/POST/*',
                    ],
                },
            ],
        },
    }
