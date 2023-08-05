import aiohttp
import logging

from common.utils import ClientResponse
from common.utils import logger
from common.rest_client.exceptions import ClientConfigurationError


class BaseClient:

    _host = None
    _port = None

    def __init__(self, headers=None):
        self.headers = headers or {'Content-Type': 'application/json'}
        self._url = f'http://{self.host}:{self.port}/'
        logger.start_logging(client=self)

    def __str__(self):
        return f'{self.__class__.__name__} {type(self)}'

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def url(self):
        return self._url

    async def _request(self, method, api_uri, params: dict = None, headers: dict = {}, data: dict = None)\
            -> ClientResponse:

        if not self.port and self.host:
            logging.error(f"port and/or host variable missed for {self}", exc_info=True)
            raise ClientConfigurationError(f"port and/or host variable missed for {self}")

        if not data:
            data = {}
        if data and "Content-Type" not in headers:
            headers.update(self.headers)

        request_url = f"{self.url}/{api_uri}"
        logging.info(f'request from {self.__class__.__name__}: {method} {request_url} {params}, with {data}')

        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=request_url, data=data, headers=headers) as response:
                try:
                    request_json = await response.json()
                # type: ignore
                except aiohttp.ContentTypeError:
                    return ClientResponse(raw_content=response.content, status=response.status,
                                          headers=response.headers)

                try:
                    data = request_json["data"]
                    return ClientResponse(json=data, status=response.status, headers=response.headers)
                except (KeyError, TypeError):
                    return ClientResponse(json=request_json, status=response.status, headers=response.headers)


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

    async def options(self, api_uri, params=None, **kwargs):
        return await self._request('OPTIONS', api_uri=api_uri, params=params, **kwargs)
