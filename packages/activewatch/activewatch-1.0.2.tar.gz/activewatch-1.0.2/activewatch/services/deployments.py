# -*- coding: utf-8 -*-

from ..service import Service

class Deployments(Service):

    def __init__(self, session, *args, **kwargs):
        Service.__init__(self, "deployments", "v1", session)

    def create_deployment(self, deployment_json, account_id = None):
        return self.post(json_data=deployment_json, account_id = account_id, path_parts = [self.name])

    def delete_deployment(self, deployment_id, account_id = None):
        return self.delete(path_parts = [self.name, deployment_id], account_id = account_id)

    def get_deployment(self, deployment_id, account_id=None):
        return self.get(path_parts = [self.name, deployment_id], account_id = account_id)

    def list_deployments(self, account_id=None, filters=None):
        return self.get(account_id = account_id, path_parts = [self.name], query_params=filters)

    def update_deployment(self, deployment_id, deployment_json, account_id=None):
        return self.put(path_parts = [self.name, deployment_id], json_data=deployment_json, account_id = account_id)

