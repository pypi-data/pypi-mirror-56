import asyncio
from rest_client.base_clients import BaseClient

# example
if __name__ == "__main__":
    async def main():
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        client = BaseClient(host='http://localhost', port=8000, headers=headers)
        print(client.url)

        async with await client.put(api_uri='parse-links/1/teams') as resp:
            print(resp)
            print(await resp.read())

        async with await client.get(api_uri='parse-links/1/teams') as resp:
            print(resp)
            print(await resp.json())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
