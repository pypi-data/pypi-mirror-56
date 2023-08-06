# -*- coding: utf-8 -*-

"""
    activewatch.session
    ~~~~~~~~~~~~~~
    activewatch authentication/authorization
"""
import requests
from activewatch import client
from activewatch.region import Region


class AuthenticationException(Exception):
    def __init__(self, message):
        super(AuthenticationException, self).__init__("authentication error: {}".format(message))


class Session():
    """
    Authenticates against Alert Logic ActiveWatchaims service and stores session information (token and account id),
    additionally objects of this class can be used as auth modules for the requests lib, more info:
    http://docs.python-requests.org/en/master/user/authentication/#new-forms-of-authentication
    """

    def __init__(self, access_key_id, secret_key, account_id=None, global_endpoint = "production"):
        """
        :param region: a Region object
        :param access_key_id: your Alert Logic ActiveWatchaccess_key_id or username
        :param secret_key: your Alert Logic ActiveWatchsecret_key or password
        """
        self._global_endpoint = Region.get_global_endpoint(global_endpoint)
        self._authenticate(access_key_id, secret_key, account_id)

    def _authenticate(self, access_key_id, secret_key, account_id):
        """
        Authenticates against alertlogic ActiveWatch Access and Identity Management Service (AIMS)
        more info:
        https://console.cloudinsight.alertlogic.com/api/aims/#api-AIMS_Authentication_and_Authorization_Resources-Authenticate
        """
        try:
            auth = requests.auth.HTTPBasicAuth(access_key_id, secret_key)
            print("Path: {}/aims/v1/authenticate".format(self._global_endpoint))
            response = requests.post(self._global_endpoint + "/aims/v1/authenticate", auth=auth)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise AuthenticationException("invalid http response {}".format(e))

        try:
            self._token = response.json()["authentication"]["token"]
        except (KeyError, TypeError, ValueError):
            raise AuthenticationException("token not found in response")

        if account_id == None:
            try:
                self.account_id = response.json()["authentication"]["account"]["id"]
            except (KeyError, TypeError, ValueError):
                raise AuthenticationException("account id not found in response")
        else:
            self.account_id = account_id

        try:
            self.account_name = response.json()["authentication"]["account"]["name"]
        except (KeyError, TypeError, ValueError):
            raise AuthenticationException("account name not found in response")
        
    def __call__(self, r):
        """
        requests lib auth module callback
        """
        r.headers["x-aims-auth-token"] = self._token
        return r

    def client(self, service_name, *args, **kwargs):
        return client(service_name, self, *args, **kwargs)

    def get_account_id(self):
        return self.account_id
# activewatch.client.connect(session, 'deployments', cid=1234)
