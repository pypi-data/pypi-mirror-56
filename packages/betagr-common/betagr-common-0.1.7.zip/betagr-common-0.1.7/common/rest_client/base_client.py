import aiohttp
import logging
import json

from common.utils import client_response as ClientResponse
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
        return self._host.rstrip('/')

    @property
    def port(self):
        return self._port

    @property
    def url(self):
        return self._url

    async def _request(self, method, api_uri, params=None, headers=None, data=None, **kwargs)\
            -> ClientResponse:

        if not (self.port and self.host):
            msg = f"ClientConfigurationError: port and/or host variables are missed for {self}"
            logging.error(msg, exc_info=True)
            raise ClientConfigurationError(msg)

        if not headers:
            headers = self.headers

        if data and "content-type" not in map(str.lower, headers):
            headers.update({'Content-Type': 'application/json'})

        request_url = f"{self.url}{api_uri.lstrip('/')}"

        async with aiohttp.ClientSession() as session:
            async with session.request(method=method,
                                       url=request_url,
                                       params=params,
                                       json=data,
                                       headers=headers) as resp:

                logging.info(f'{self.__class__.__name__} sent request: {method} {resp.url} '
                             f'with data: type({type(data)}){data}')

                try:
                    data = await resp.json()
                # type: ignore
                except aiohttp.ContentTypeError as e:
                    logging.error(msg=e, exc_info=True)
                    return ClientResponse(status=resp.status, reason=resp.reason,
                                          headers=resp.headers,
                                          json={}, raw_content=await resp.read())

                return ClientResponse(status=resp.status, reason=resp.reason,
                                      headers=resp.headers,
                                      json=data, raw_content=json.dumps(data))


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
