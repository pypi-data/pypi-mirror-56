# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime, timedelta

from ibm_ai_openscale.data_mart import DataMart
from ibm_ai_openscale.utils import *
from ibm_ai_openscale.clients_manager import ClientsManager


'''
.. module:: APIClient
   :platform: Unix, Windows
   :synopsis: Watson OpenScale API Client.

.. moduleauthor:: IBM
'''


class APIClientBase:
    """
    Watson OpenScale client.

    :var data_mart: Manage db connection
    :vartype data_mart: DataMart
    :var version: Returns version of the python library.
    :vartype version: str
    """
    def __init__(self, aios_credentials):
        self._logger = logging.getLogger(__name__)
        self._service_credentials = aios_credentials
        self.version = version()
        self._href_definitions = AIHrefDefinitions(aios_credentials)
        self._token = self._create_token() if 'iam_token' not in aios_credentials else aios_credentials['iam_token']
        self.data_mart = DataMart(self)
        self._clients_manager = ClientsManager(self.data_mart.bindings)
        self._logger.info(u'Client successfully initialized')

    def _get_headers(self, content_type='application/json', no_content_type=False):
        validate_type(content_type, "content_type", str, True)
        validate_type(no_content_type, "no_content_type", bool, True)

        headers = {
            'Authorization': 'Bearer ' + self._get_token(),
            'Origin': 'cli://python_client'
        }

        if not no_content_type:
            headers.update({'Content-Type': content_type})

        if 'headers' in self._service_credentials:
            headers.update(self._service_credentials['headers'])

        return headers

    def _get_token(self):
        if self._token is None:
            self._token = self._create_token()
        elif 'apikey' in self._service_credentials and self._get_expiration_datetime() - timedelta(minutes=30) < datetime.now():
            self._refresh_token()
        elif self._get_expiration_datetime() < datetime.now():
            raise ClientError('Token expired.')

        return self._token

    def _create_token(self):
        raise NotImplemented()

    def _refresh_token(self):
        self._token = self._create_token() # TODO - something more ambitious?

    def _get_expiration_datetime(self):
        token_parts = self._token.split('.')
        token_padded = token_parts[1] + '=' * (len(token_parts[1]) % 4)
        token_info = json.loads(base64.b64decode(token_padded, '-_').decode('utf-8'))
        token_expire = token_info.get('exp')

        return datetime.fromtimestamp(token_expire)