import base64
import json
import logging
import os

import boto3
import botocore

COGNITO = boto3.client('cognito-idp')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
LOG_LEVEL = os.getenv('LOG_LEVEL') or 'INFO'
LOG_FORMAT = os.getenv('LOG_FORMAT') or '%(levelname)s %(reqid)s %(message)s'


class SuppressFilter(logging.Filter):
    """
    Suppress Log Records from registered logger

    Taken from ``aws_lambda_powertools.logging.filters.SuppressFilter``
    """
    def __init__(self, logger):
        self.logger = logger

    def filter(self, record):
        logger = record.name
        return False if self.logger in logger else True


class LambdaLoggerAdapter(logging.LoggerAdapter):
    """
    Lambda logger adapter.
    """
    def __init__(self, name, level=None, format_string=None):
        # Get logger, formatter
        logger = logging.getLogger(name)

        # Set log level
        logger.setLevel(level or LOG_LEVEL)

        # Set handler if necessary
        if not logger.handlers:  # and not logger.parent.handlers:
            formatter = logging.Formatter(format_string or LOG_FORMAT)
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # Suppress AWS logging for this logger
        for handler in logging.root.handlers:
            logFilter = SuppressFilter(name)
            handler.addFilter(logFilter)

        # Initialize adapter with null RequestId
        super().__init__(logger, dict(reqid='-'))

    def attach(self, handler):
        """
        Decorate Lambda handler to attach logger to AWS request.

        :Example:

        >>> logger = lambo.getLogger(__name__)
        >>>
        >>> @logger.attach
        ... def handler(event, context):
        ...     logger.info('Hello, world!')
        ...     return {'ok': True}
        ...
        >>> handler({'fizz': 'buzz'})
        >>> # => INFO RequestId: {awsRequestId} EVENT {"fizz": "buzz"}
        >>> # => INFO RequestId: {awsRequestId} Hello, world!
        >>> # => INFO RequestId: {awsRequestId} RETURN {"ok": True}
        """
        def wrapper(event=None, context=None):
            try:
                self.addContext(context)
                self.info('EVENT %s', json.dumps(event, default=str))
                result = handler(event, context)
                self.info('RETURN %s', json.dumps(result, default=str))
                return result
            finally:
                self.dropContext()
        return wrapper

    def addContext(self, context=None):
        """
        Add runtime context to logger.
        """
        try:
            reqid = f'RequestId: {context.aws_request_id}'
        except AttributeError:
            reqid = '-'
        self.extra.update(reqid=reqid)
        return self

    def dropContext(self):
        """
        Drop runtime context from logger.
        """
        self.extra.update(reqid='-')
        return self


logger = LambdaLoggerAdapter('PyPI.Authorizer')


@logger.attach
def handler(event, context=None):
    """
    Basic auth.
    """
    # Extract values from event
    try:
        authorization_token = event['headers']['authorization']
    except KeyError:  # pragma: no cover
        return dict(isAuthorized=False)

    # Decode creds
    username, password = decode_creds(authorization_token)

    # Attempt to authorize
    return authorize(username, password)


def decode_creds(authorization_token):
    """
    Decode Basic auth token into username, password.

    :param str authorization_token: Basic auth token
    :returns tuple: (username, password)
    """
    try:
        _, auth64 = authorization_token.split(' ')
        username, password = base64.b64decode(auth64).decode().split(':')
    except (AttributeError, ValueError):  # pragma: no cover
        username = password = None
    return (username, password)


def authorize(username, password):
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
        return dict(isAuthorized=True)
    except botocore.exceptions.ClientError as err:
        logger.error(err)
        return dict(isAuthorized=False)
