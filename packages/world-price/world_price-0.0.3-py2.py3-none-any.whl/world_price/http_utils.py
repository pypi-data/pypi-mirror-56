import aiohttp
import logging

logger = logging.getLogger("HTTP_UTIL")


async def get(url, headers=None, params=None, timeout=10):
    async with aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(timeout)
    ) as session:

        async with session.get(url, params=params) as resp:

            try:

                return await resp.json(
                    content_type=None,  # disable content-type validation
                )

            except Exception as e:

                logger.error(e)

                raise e


async def post(url, headers=None, params=None, data=None, json=None, timeout=10):
    if data is not None and json is not None:
        raise ValueError('data and json parameters can not be used at the same time')

    async with aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(timeout)
    ) as session:

        async with session.post(url, params=params, data=data, json=json) as resp:

            try:

                return await resp.json(
                    content_type=None,  # disable content-type validation
                )

            except Exception as e:

                logger.error(e)

                raise e
