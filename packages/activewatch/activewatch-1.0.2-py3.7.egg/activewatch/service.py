# -*- coding: utf-8 -*-

import binascii
import os
import json
import requests
from activewatch.region import Residency
from activewatch.region import EndpointType

class InvalidEndpointCall(Exception):
    pass

class InvalidResponse(Exception):
    pass

class Service:

    def __init__(self, name, version='v1', session=None, residency=None):
        self.name = name
        self.set_session(session)
        self.version = version
        self.residency = residency if residency != None else Residency.DEFAULT.value
        self._get_service_endpoint()

    def _get_service_endpoint(self):
        try:
            url = "{}/endpoints/v1/{}/residency/{}/services/{}/endpoint/{}".format(
                                                            self._session._global_endpoint,
                                                            self._session.account_id,
                                                            self.residency,
                                                            self.name,
                                                            EndpointType.API.value)
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise InvalidEndpointCall(e)

        try:
            self.endpoint = response.json()[self.name]
        except (KeyError, TypeError, ValueError):
            raise InvalidResponse("service not found in response for {}".format(url))

    def _get_account_id(self, account_id, top_level):
        if top_level:
            return None
        elif account_id is None:
            return self._session.account_id
        else:
            return account_id

    def _get_global_endpoint(self):
            return self._session._global_endpoint

    def set_session(self, session):
        """ changes current session, this session object is used to authenticate
         api calls
        :param session: an authenticated alertlogic.auth.Session object
        """
        self._session = session

    def get(self, 
            version=None, account_id=None,
            path_parts=None, query_params=None, headers=None,
            json_data=None, top_level=False):
        return self.call_endpoint('GET', 
                version,
                self._get_account_id(account_id, top_level),
                path_parts,
                headers,
                query_params,
                json_data)

    def post(self,
            version=None, account_id=None,
            path_parts=None, query_params=None, headers=None,
            json_data=None, top_level=False):
        return self.call_endpoint('POST', 
                version,
                self._get_account_id(account_id, top_level),
                path_parts,
                headers,
                query_params,
                json_data)

    def post_multipart(self, metadata, result, version=None, account_id=None,
                path_parts=None, query_params=None, headers=None,
                json_data=None, top_level=False):
        url = self.build_url(version, self._get_account_id(account_id, top_level), path_parts)
        payload = {
                "metadata": json.dumps(metadata),
                "result": json.dumps(result)
        }
        data, content_type = self._encode_multipart_formdata(payload)
        request_headers = {
            "content-type": content_type,
            "content-length": str(len(data)),
        }
        return requests.post(url, headers = request_headers, data = data, auth=self._session)

    def put(self,
            version=None, account_id=None,
            path_parts=None, query_params=None, headers=None,
            json_data=None, top_level=False):
        return self.call_endpoint('PUT',
                version,
                self._get_account_id(account_id, top_level),
                path_parts,
                headers,
                query_params,
                json_data)

    def delete(self, version=None, account_id=None,
                path_parts=None, query_params=None, headers=None,
                json_data=None, top_level=False):
        return self.call_endpoint('DELETE',
                version,
                self._get_account_id(account_id, top_level),
                path_parts,
                headers,
                query_params,
                json_data)

    def call_endpoint(self, method, version, account_id, path_parts, headers, query_params, json_data):
        url = self.build_url(version, account_id, path_parts)
        print("Executing request: {} {}: ".format(method, url))
        try:
            return requests.request(method, url, params=query_params, headers=headers, json=json_data, auth=self._session)
        except requests.exceptions.HTTPError as e:
            raise InvalidEndpointCall(e.message)

    def build_url(self, version, account_id, path_parts):
        parts = path_parts if path_parts != None else []
        v = self.version if version is None else version
        if self.version is None:
            path = "/".join([self.name] + path_parts)
        elif account_id is None:
            path = "/".join([self.name, v] + parts)
        else:
            path = "/".join([self.name, v, account_id] + parts)
        return "https://{}/{}".format(self.endpoint, path)

    @staticmethod
    def _encode_multipart_formdata(fields):
        boundary = binascii.hexlify(os.urandom(16)).decode('ascii')
        body = (
            "".join("--%s\r\n"
                    "Content-Disposition: form-data; name=\"%s\"\r\nContent-Type: application/json\r\n"
                    "\r\n"
                    "%s\r\n" % (boundary, field, value)
                    for field, value in fields.items()) +
            "--%s--\r\n" % boundary
        )
        content_type = "multipart/form-data; boundary=%s" % boundary
        return body, content_type

