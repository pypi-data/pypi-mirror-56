# -*- coding: utf-8 -*-

import json
import time
from ..service import Service

class Scan_result(Service):
    # https://console.account.alertlogic.com/users/api/scan_result/
    def __init__(self, session, version=None, account_id = None):
        Service.__init__(self, "scan_result", version if version != None else "v1", session)

    def get_last_cleanup_time(self):
        return self.get(path_parts = ['last_cleanup_time'], top_level=True)

    def add_scan_result(self, 
                    scanner,
                    scope,
                    deployment_id,
                    asset_id,
                    snapshot_id,
                    result,
                    content_type = "application/json",
                    account_id = None):
        metadata = {
            "scanner": scanner,
            "scanner_scope": scope,
            "asset_id": asset_id,
            "environment_id": deployment_id,
            "scan_policy_snapshot_id": snapshot_id,
            "timestamp": int(time.time()),
            "content_type": content_type
        }
        return self.post_multipart(metadata, result, account_id = account_id)

    def get_scan_result(self, deployment_id, result_id, account_id = None):
        return self.get(version = "v2", path_parts = [deployment_id, result_id, "result"])

    def get_scan_result_metadata(self, deployment_id, result_id, account_id = None):
        return self.get(version = "v2", path_parts = [deployment_id, result_id, "metadata"])

