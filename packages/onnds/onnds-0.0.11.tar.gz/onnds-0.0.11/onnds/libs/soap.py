import requests
import os
import sys


class DsSoap:
    def __init__(self, logger):
        self.logger = logger
        self.logger.entry('info', 'Initiating connection to SOAP API & obtaining SOAP API key')

        dsm_address = os.environ.get('DS_ADDRESS', 'https://app.deepsecurity.trendmicro.com')
        self.soap_url = f'{dsm_address}/rest'
        auth_url = f'{self.soap_url}/authentication/login'

        payload = {
            'dsCredentials':
                {
                    'userName': os.environ['DS_USERNAME'],
                    'password': os.environ['DS_PASSWORD'],
                }
        }

        tenant_name = os.environ.get('DS_TENANT')
        if tenant_name:
            payload['dsCredentials']['tenantName'] = tenant_name

        else:
            auth_url = f'{auth_url}/primary'

        self.session = requests.Session()
        r = self.session.post(auth_url, json=payload)
        self._check_api_response(r, error_msg='Could not obtain SOAP API SID:')

        sid = r.text
        self.session.cookies.set('sID', sid)

    def add_aws_account(self):
        url = f'{self.soap_url}/cloudaccounts/aws'

        self.logger.entry('info', f'Obtaining AWS access & secret keys')
        try:
            aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
            aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']

        except KeyError:
            msg = '"AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY" environment variables must be set in order to add ' \
                  'AWS cloud connectors'
            self.logger.entry('critical', msg)
            sys.exit(msg)

        self.logger.entry('info', f'Adding AWS account using the Cloud Connector address {url}')
        payload = {
            'AddAwsAccountRequest': {
                'awsCredentials': {
                    'accessKeyId': aws_access_key,
                    'secretKey': aws_secret_key,
                }
            },
        }

        r = self.session.post(url, json=payload)
        self._check_api_response(r, error_msg='Could not add AWS cloud account:')

        self.logger.entry('info', 'Successfully added AWS cloud account')

    def _check_api_response(self, response, error_msg):
        if response.status_code is not 200:
            msg = f'{error_msg} {response.text}'
            self.logger.entry('critical', msg)
            sys.exit(msg)
