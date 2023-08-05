import os

from common.rest_client.base_client import BaseClient


class BaseClientParser(BaseClient):

    _host = os.getenv('PARSER_API_HOST')
    _port = int(os.getenv('PARSER_API_PORT'))

    def __init__(self, headers=None):
        super().__init__(headers=headers)

    async def get_all_teams(self):
        url = '/parse-links?parse_by=teams'
        response = await self.get(api_uri=url)
        return response.json

    async def get_teams_by_link(self, link_id):
        url = '/parse-links/{link_id}?parse_by=teams'.format(link_id=link_id)
        response = await self.get(api_uri=url)
        return response

    async def put_teams_by_link(self, link_id):
        url = '/parse-links/{link_id}?parse_by=teams'.format(link_id=link_id)
        response = await self.put(api_uri=url)
        return response.json

    async def delete_teams_by_link(self, link_id):
        url = '/parse-links/{link_id}?parse_by=teams'.format(link_id=link_id)
        response = await self.delete(api_uri=url)
        return response.json

    async def get_real_teams(self):
        url = '/real-teams'
        response = await self.get(api_uri=url)
        return response.json

    async def put_real_teams(self):
        url = '/real-teams'
        response = await self.put(api_uri=url)
        return response.json