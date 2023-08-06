import aiohttp
import logging

from utils import logger as log
from utils.utils import prepared_data


class BaseClient:

    def __init__(self, host=None, port=None, headers=None):
        self.headers = headers or {'Content-Type': 'application/jon'}
        self._host = host
        self._port = port
        self._cookies = {}
        self._url = f'{self._host}:{self._port}/'
        log.start_logging(client=self)

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def url(self):
        return self._url

    async def _request(self, method,api_uri, params=None, data=None, **kwargs):
        url = self.url + api_uri
        # console log
        logging.debug(f'request from {self.__class__.__name__}: {method} {url} {params}, with {data}')
        # convert data to aiohttp.DataForm
        data = prepared_data(data)

        return aiohttp.request(method=method, url=url, params=params, data=data, **kwargs)

    async def get(self, api_uri, params=None, **kwargs):
        return await self._request('GET', api_uri=api_uri, params=params, **kwargs)

    async def post(self, api_uri, params=None, data=None, **kwargs):
        return await self._request('POST', api_uri=api_uri, params=params, data=data, **kwargs)

    async def put(self, api_uri, params=None, data=None, **kwargs):
        return await self._request('PUT', api_uri=api_uri, params=params, data=data, **kwargs)

    async def patch(self, api_uri, params=None, data=None, **kwargs):
        return await self._request('PATCH', api_uri=api_uri, params=params, data=data, **kwargs)

    async def delete(self, api_uri, params=None, **kwargs):
        return await self._request('DELETE', api_uri=api_uri, params=params, **kwargs)


class BaseClientSSO(BaseClient):
    """Base api client that describes full standard api for SSO service.
    _api_uri should contains the [key:value, ..] in form [method_name: api_uri which is used by the method, ..]"""

    def __init__(self, host, port, headers=None):
        super().__init__(host=host, port=port, headers=headers)
        self._api_uri = {
            'sign_up': 'sign-up',
            'sign_in': 'sign-in',
            'sign_out': 'sign-out',
            'reset_password': 'reset-password',
        }

    async def sign_up(self, body):
        url = self._api_uri['sign_up']
        return await self.post(url, body=body, cookies=self._cookies)

    async def sign_in(self, body):
        url = self._api_uri['sign_in']
        return await self.post(url, body=body, cookies=self._cookies)

    async def sign_out(self):
        url = self._api_uri['sign_out']
        return await self.post(url, cookies=self._cookies)

    async def reset_password(self, body):
        url = self._api_uri['reset_password']
        return await self.patch(url, body=body, cookies=self._cookies)


class BaseClientParser(BaseClient):
    def __init__(self, host, port, headers=None):
        super().__init__(host, port, headers=headers)

        self._api_uri = {
            'all_teams': 'parse-links/teams',
            'teams_by_link': 'parse-links/{link_id}/teams',
            'real_teams': 'real-teams',
        }

    async def get_all_teams(self):
        url = self._api_uri['all_teams']
        async with await super().get(url, cookies=self._cookies, params=None) as response:
            return await response.json()

    async def get_teams_by_link(self, link_id):
        url = self._api_uri['teams_by_link'].format(link_id=link_id)
        async with await super().get(url, cookies=self._cookies, params=None) as response:
            if response.status == 404:
                return {"status": response.status}
            return {"json": await response.json(), "status": response.status}

    async def put_teams_by_link(self, link_id):
        url = self._api_uri['teams_by_link'].format(link_id=link_id)
        async with await super().put(url, cookies=self._cookies, params=None) as response:
            return await response.text()

    async def delete_teams_by_link(self, link_id):
        url = self._api_uri['teams_by_link'].format(link_id=link_id)
        async with await super().delete(url, cookies=self._cookies, params=None) as response:
            return await response.text()

    async def get_real_teams(self):
        url = self._api_uri['real_teams']
        async with await super().get(url, cookies=self._cookies, params=None) as response:
            return await response.json()

    async def put_real_teams(self):
        url = self._api_uri['real_teams']
        async with await super().put(url, cookies=self._cookies, params=None) as response:
            return await response.text()


class BaseClientAggregator(BaseClient):
    def __init__(self, host, port, headers=None):
        super().__init__(host, port, headers=headers)

        self._api_uri = {
            'aggregator': 'aggregator',
            'aggregator_by_link': 'aggregator/{link_id}',
        }

    async def aggregator(self, team=None):
        url = self._api_uri['aggregator']
        if team:
            url = f"{url}/?team={team}"
        async with await super().get(url, cookies=self._cookies, params=None) as response:
            return await response.json()

    async def aggregator_by_link(self, link_id, team=None):
        url = self._api_uri['aggregator_by_link'].format(link_id=link_id)
        if team:
            url = f"{url}/?team={team}"
        async with await super().get(url, cookies=self._cookies, params=None) as response:
            return await response.json()
