hypy
====
A basic Hypixel API wrapper

Notice
------
This project has been unmaintained since 2022, and probably does not work anymore following the `API Changes <https://hypixel.net/threads/public-api-changes-february-2023.5266129/>`__ in February of 2023. 


covering:

| /punishmentstats
| /key
| /player
| /resources/skyblock/skills
| /skyblock/auctions
| /skyblock/profile
| /friends
| /status
| /guild
| /counts

Documentation
-------------
https://hypy.readthedocs.io/en/latest/index.html

Quickstart
----------

1. Install hypy:
    .. code-block:: sh

        $ pip install hypy-hypixel
2. Create a Hypixel object::
    .. code-block:: py

        from hypy import Hypixel
        
        hypixel = Hypixel(api_key)
        await hypixel.setup()

Credits
-------

| https://github.com/aio-libs/aiohttp
| https://github.com/twoolie/NBT
| https://github.com/ijl/orjson
| https://pypi.org/project/aiofiles/
| https://github.com/Senither/Hypixel-Skyblock-Leaderboard for the weight calculations
| https://github.com/Altpapier/SkyHelperAPI for the networth api
