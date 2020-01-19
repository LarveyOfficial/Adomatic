import Config
import pymongo
import asyncio

cache = []

async def update_cache():
    servers = Config.SERVERS.find({})
    new_cache = []
    for server in servers:
        if server["announce"] is not None:
            new_cache.append(server)
    global cache
    cache = new_cache
