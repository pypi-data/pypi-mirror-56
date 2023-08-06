# -*- coding: utf-8 -*-

import urllib
from activewatch import NoValue
from activewatch.session import AuthenticationException
from activewatch.session import Session
from activewatch.service import Service

"""
    alertlogic.services.aims
    ~~~~~~~~~~~~~~
    alertlogic aims service client
"""

"""
List of valid relationships
"""
class AimsRelationship(NoValue):
    BILLS_TO    = 'bills_to'
    MANAGED     = 'managed'
    MANAGING    = 'managing'

class Aims(Service):
    # https://console.cloudinsight.alertlogic.com/api/aims/
    def __init__(self, session, version=None, account_id = None):
        Service.__init__(self, "aims", version if version != None else "v1", session)

    # /aims/v1/:account_id/account
    def get_account_details(self, account_id):
        return self.get(account_id = account_id, path_parts = ["account"])

    # /aims/v1/:account_id/accounts/:relationship/:related_account_id
    # returns status_code:
    # 204 - relationship is found
    # 404 - relationship isn't found
    # 403 - Forbidden, 
    # 410 - Gone
    def get_account_relationship(self, related_account_id, relationship=AimsRelationship.MANAGED, account_id=None):
        return self.get(account_id = account_id, path_parts = ["accounts", relationship.value, related_account_id])

    # /aims/v1/accounts/name/:name
    # returns request object 
    def get_account_details_by_name(self, name):
        return self.get(path_parts = ["accounts", "name", urllib.parse.quote(name)], top_level=True)
    
    # /aims/v1/:account_id/account_ids/:relationship?active=:active
    def list_account_ids_by_relationship(self, account_id=None, relationship=AimsRelationship.MANAGED, active=True):
        return self.get(account_id = account_id,
                        path_parts = ['account_ids', relationship.value],
                        query_params = {'active': str(active).lower()})

    # /aims/v1/:account_id/accounts/:relationship?active=:active
    def list_accounts_by_relationship(self, account_id=None, relationship=AimsRelationship.MANAGED, active=True):
        return self.get(account_id = account_id,
                        path_parts = ['accounts', relationship.value],
                        query_params = {'active': str(active).lower()})

    # /aims/v1/:account_id/account
    def update_account_detauls(self, account_id=None, mfa_required=False):
        return self.post(account_id=account_id,
                        path_parts=["account"],
                        query_params = {'mfa_required': str(mfa_required).lower()})

    def authenticate(self, user_name, password):
        try:
            session = Session(
                    access_key_id=user_name,
                    secret_key=password,
                    global_endpoint=self._get_global_endpoint()) 
        except AuthenticationException as e:
            raise e
        return session

    # /aims/v1/change_password
    def change_user_password(self, email, current_password, new_password):
        return self.post(path_parts = ["change_password"],
                        query_params = {
                            'email': email,
                            'current_password': current_password,
                            'new_password': new_password
                        },
                        top_level=True)

    # /aims/v1/token_info
    def get_token_info(self, token_info):
        return self.get(path_parts = ["token_info"], headers={'X-Aims-Auth-Token': token_info})

    # /aims/v1/reset_password
    def reset_password(self, email, return_to):
        return self.post(
                path_parts = ["reset_password"],
                json_data = {'email': email, 'return_to': return_to},
                top_level=True)

    # /aims/v1/reset_password/:token
    def reset_password(self, token, password):
        return self.put(path_parts = ["reset_password", token], json_data = {'password': password}, top_level=True)

    # /aims/v1/:account_id/roles
    def create_role(self, name, permissions, account_id=None):
        return self.post(
                account_id=account_id,
                path_parts=["roles"],
                json_data = {
                    'name': name,
                    'permissions': permissions
                })

    # /aims/v1/:account_id/roles/:role_id
    def delete_role(self, role_id, account_id=None):
        return self.delete(account_id=account_id, path_parts=['roles', role_id])

    # /aims/v1/roles/:role_id
    def get_global_role_details(self, role_id):
        return self.get(path_parts=['roles', role_id], top_level=True)

    # /aims/v1/:account_id/roles/:role_id
    def get_role_details(self, role_id, account_id=None):
        return self.get(account_id=account_id, path_parts=['roles', role_id])

    # /aims/v1/roles
    def list_global_roles(self):
        return self.get(path_parts=['roles'], top_level=True)

    # /aims/v1/:account_id/roles
    def list_roles(self, account_id=None):
        return self.get(account_id=account_id, path_parts=['roles'])

    # /aims/v1/:account_id/roles/:role_id
    def update_role(self, role_id, account_id=None, name=None, permissions=None):
        json_body = dict()
        if name is not None:
            json_body.add('name', name)
        elif permissions is not None:
            json_body.add('permissions', permissions)
        else:
            raise ValueError('Expected either name, permissions or both arguments.')
        return self.post(account_id=account_id, path_parts=['roles'], json_data=json_body) 

    # /aims/v1/:account_id/users/:user_id/access_keys
    def create_access_key(self, user_id, account_id=None):
        return self.post(account_id=account_id, path_parts=['users', user_id, 'access_keys'])

    # /aims/v1/:account_id/users/:user_id/access_keys/:access_key_id
    def delete_access_key(self, user_id, access_key_id, account_id=None):
        return self.delete(self, account_id=account_id,
                path_parts=['users', user_id, 'access_keys', access_key_id])

    # /aims/v1/:account_id/users?one_time_password=:one_time_password
    def create_user(self, user_parameters, account_id=None, one_time_password=False):
        if 'name' not in user_parameters and 'email' not in user_parameters:
            raise ValueError('Expected name and email keys to be in user_parameters')

        return self.post(account_id=account_id,
                        path_parts=['users'],
                        query_params={'one_time_password', str(one_time_password).lower()},
                        json_data=user_parameters)

    # /aims/v1/:account_id/users/:user_id
    def delete_user(self, user_id, account_id=None):
        return self.delete_user(account_id=account_id, path_parts=['users', user_id])

    # /aims/v1/access_keys/:access_key_id
    def get_access_key(self, access_key_id):
        return self.get(path_parts=['access_keys', access_key_id], top_level=True)

    # /aims/v1/:account_id/users/:user_id/role_ids
    def get_user_role_ids(self, user_id, account_id=None):
        return self.get(account_id=account_id, path_parts=['users', user_id, 'role_ids'])

    # /aims/v1/:account_id/users/:user_id/roles
    def get_user_roles(self, user_id, account_id=None):
        return self.get(account_id=account_id, path_parts=['users', user_id, 'roles'])

    # /aims/v1/:account_id/users/:user_id
    def get_user_details(self, user_id, account_id=None):
        return self.get(account_id=account_id, path_parts=['users', user_id])

    # /aims/v1/user/:user_id
    def get_user_by_id(self, user_id,
            include_role_ids=False, include_user_credential=False, include_access_keys=False):
        query_params = dict()
        if include_access_keys == True:
            query_params.add('include_role_ids', 'true')
        if include_user_credential == True:
            query_params.add('include_user_credential', 'true')
        if include_access_keys == True:
            query_params.add('include_access_keys', 'true')
        return self.get(path_parts=['user', user_id], query_params=query_params)

    # /aims/v1/user/username/:username
    def get_user_by_name(self, user_name,
            include_role_ids=False, include_user_credential=False, include_access_keys=False):
        query_params = dict()
        if include_access_keys == True:
            query_params.add('include_role_ids', 'true')
        if include_user_credential == True:
            query_params.add('include_user_credential', 'true')
        if include_access_keys == True:
            query_params.add('include_access_keys', 'true')
        return self.get(path_parts=['username', user_name], query_params=query_params)

    # /aims/v1/:account_id/users/:user_id/permissions
    def get_user_permissions(self, user_id, account_id=None):
        return self.get(account_id=account_id, path_parts=['users', user_id, 'permissions'])

    # /aims/v1/:account_id/users/:user_id/roles/:role_id
    def grant_user_role(self, user_id, role_id, account_id=None):
        return self.put(account_id=account_id, path_parts=['users', user_id, 'roles', role_id])
