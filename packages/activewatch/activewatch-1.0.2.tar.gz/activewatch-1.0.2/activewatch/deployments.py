from activewatch.service import Service

class Deployments(Service):

    def __init__(self, session):
        Service.__init__(self, "deployments", "v1", session)

    def create_deployment(self, account_id, deployment_json):
        return self.post([account_id, "deployments"], json=deployment_json)

    def delete_deployment(self, account_id, deployment_id):
        return self.delete([account_id, "deployments", deployment_id])

    def get_deployment(self, account_id, deployment_id):
        return self.get([account_id, "deployments", deployment_id])

    def list_deployments(self, account_id):
        return self.get([account_id, "deployments"])

    def update_deployment(self, account_id, deployment_id, deployment_json):
        return self.put([account_id, "deployments", deployment_id], json=deployment_json)
