import aiohttp
import asyncio
import re


async def call_api(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

def sort_keyval(d):
    key, value = d
    return value, int(key)

def sort_list_query(lst: list,query: str,value:str|int):
    if type(value) == int:
        return list(filter(lambda x: x[query] == value, lst))
    elif type(value) == str:
        return list(filter(lambda x: re.search(value,x[query]), lst))
    else:
        return lst