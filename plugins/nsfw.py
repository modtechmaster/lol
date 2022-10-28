
"""RIP of original plugin and modify for ultroid by @moon_knight69 and @itzyournil 
✘ Commands Available
──「 **Danbooru Search** 」──
-> `.animu`(search string) or `.aninsfw`(search nsfw string)
Search images from Danbooru.
FOR Real NSFW Content
`.boobs` (search random boobs pic)
`.butts `(search random butts pic)
Enjoy
"""

import os
import urllib
from asyncio import sleep

import requests

from . import *


@ultroid_cmd(pattern="ani(mu|nsfw) ?(.*)")
async def danbooru(message):
    await message.edit("`Processing…`")

    rating = "Explicit" if "nsfw" in message.pattern_match.group(1) else "Safe"
    search_query = message.pattern_match.group(2)

    params = {
        "limit": 1,
        "random": "true",
        "tags": f"Rating:{rating} {search_query}".strip(),
    }

    with requests.get(
        "http://danbooru.donmai.us/posts.json", params=params
    ) as response:
        if response.status_code == 200:
            response = response.json()
        else:
            await message.edit(
                f"`An error occurred, response code:` **{response.status_code}**"
            )
            await sleep(5)
            await message.delete()
            return

    if not response:
        await message.edit(f"`No results for query:` __{search_query}__")
        await sleep(5)
        await message.delete()
        return

    valid_urls = [
        response[0][url]
        for url in ["file_url", "large_file_url", "source"]
        if url in response[0].keys()
    ]

    if not valid_urls:
        await message.edit(f"`Failed to find URLs for query:` __{search_query}__")
        await sleep(5)
        await message.delete()
        return
    for image_url in valid_urls:
        try:
            await message.client.send_file(message.chat_id, image_url)
            await message.delete()
            return
        except Exception as e:
            print(e)
    await message.edit(f"``Failed to fetch media for query:` __{search_query}__")
    await sleep(5)
    await message.delete()


@ultroid_cmd(pattern="boobs(?: |$)(.*)")
async def boobs(e):
    await e.edit("`Finding some big boobs...`")
    await sleep(1)
    await e.edit("`Sending some big boobs...`")
    nsfw = requests.get("http://api.oboobs.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve("http://media.oboobs.ru/{}".format(nsfw), "*.jpg")
    os.rename("*.jpg", "boobs.jpg")
    await e.client.send_file(e.chat_id, "boobs.jpg")
    os.remove("boobs.jpg")
    await e.delete()


@ultroid_cmd(pattern="butts(?: |$)(.*)")
async def butts(e):
    await e.edit("`Finding some beautiful butts...`")
    await sleep(1)
    await e.edit("`Sending some beautiful butts...`")
    nsfw = requests.get("http://api.obutts.ru/butts/0/1/random").json()[0]["preview"]
    urllib.request.urlretrieve("http://media.obutts.ru/{}".format(nsfw), "*.jpg")
    os.rename("*.jpg", "butts.jpg")
    await e.client.send_file(e.chat_id, "butts.jpg")
    os.remove("butts.jpg")
    await e.delete()

