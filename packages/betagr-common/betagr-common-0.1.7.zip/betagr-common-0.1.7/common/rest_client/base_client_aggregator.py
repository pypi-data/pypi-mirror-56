import os

from common.rest_client.base_client import BaseClient


class BaseClientAggregator(BaseClient):

    _host = os.getenv('AGGREGATOR_API_HOST')
    _port = int(os.getenv('AGGREGATOR_API_HOST'))

    def __init__(self, headers=None):
        super().__init__(headers=headers)

    async def aggregator(self, team=None):
        url = '/aggregator'
        params = {}
        if team:
            params = {'team': team}
        response = await self.get(api_uri=url, params=params)
        return response.json

    async def aggregator_by_link(self, link_id, team=None):
        url = '/aggregator/{link_id}'.format(link_id=link_id)
        params = {}
        if team:
            params = {'team': team}
        response = await self.get(api_uri=url, params=params)
        return response.json