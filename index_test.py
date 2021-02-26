import base64
from unittest import mock

import botocore.exceptions

with mock.patch('boto3.client'):
    import index


class TestHandler:
    def setup(self):
        index.COGNITO = mock.MagicMock()
        self.good = base64.b64encode('good:good'.encode()).decode()
        self.bad = base64.b64encode('bad:bad'.encode()).decode()

    def test_handler_authorized(self):
        index.COGNITO.initiate_auth.return_value = True
        event = {'headers': {'authorization': f'Basic {self.good}'}}
        assert index.handler(event) == dict(isAuthorized=True)

    def test_handler_unauthorized(self):
        index.COGNITO.initiate_auth.side_effect = \
            botocore.exceptions.ClientError(
                error_response={},
                operation_name='InitiateAuth',
            )
        event = {'headers': {'authorization': f'Basic {self.bad}'}}
        assert index.handler(event) == dict(isAuthorized=False)
