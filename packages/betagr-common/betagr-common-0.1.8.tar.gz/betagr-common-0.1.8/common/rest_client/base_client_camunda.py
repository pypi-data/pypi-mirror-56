import os

from common.rest_client.base_client import BaseClient


class BaseClientCamunda(BaseClient):

    _host = os.getenv('CAMUNDA_API_HOST')
    _port = int(os.getenv('CAMUNDA_API_PORT'))
    _url_api = 'engine-rest/engine/default'

    def __init__(self, headers=None):
        super().__init__(headers=headers)

    async def get_process_definition(self, name_process_definition):
        url = f"{self._url_api}/process-definition?name={name_process_definition}"
        response = await self.get(api_uri=url)
        return response

    async def process_definition_start(self, process_definition_id):
        url = f"{self._url_api}/process-definition/{process_definition_id}/start"
        response = await self.post(api_uri=url)
        return response

    async def get_current_task(self, process_instance_id):
        url = f"{self._url_api}/task?processInstanceId={process_instance_id}"
        response = await self.get(api_uri=url)
        return response

    async def task_complete(self, task_id, action, value):
        url = f"{self._url_api}/task/{task_id}/complete"
        req_body = {
            "variables": {
                action: {
                    "value": value,
                    "type": "Boolean"
                }
            }
        }
        response = await self.post(api_uri=url, data=req_body)
        return response
