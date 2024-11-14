import asyncio
import json
from pprint import pprint
from urllib.parse import urlencode, quote

import aiofiles
import httpx
from bs4 import BeautifulSoup

from src.core.config import settings


async def get_movie():
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                         "image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
               "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0", }
    url = (f"https://www.imdb.com/search/title/?title_type=feature&release_date=2023-01-01,2023-12-31&num_votes=1000,"
           f"&genres=!documentary,!short&languages=en&sort=num_votes,desc")
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        res = response.text
        soup = BeautifulSoup(res, 'html.parser')
        all_titles = soup.find_all('h3', class_='ipc-title__text')
        print(len(all_titles))
        for title in all_titles:
            with open("movie.txt", mode='a', encoding='utf-8') as f:
                f.write(f"{title.text}\n")


# asyncio.run(get_movie())


async def api_movie():
    list_movie = []
    result_list = []

    async with aiofiles.open("movie.txt", mode='r', encoding='utf-8') as f:
        async for line in f:
            title = urlencode({"t": line})
            list_movie.append(title)

    async with httpx.AsyncClient() as client:
        for movie in list_movie:
            url = f"https://www.omdbapi.com/?i=tt3896198&apikey={settings.movie_api}&{movie}&y=2023&plot=full"
            response = await client.get(url)
            result_list.append(response.json())

    async with aiofiles.open("result_movie.json", "w", encoding='utf-8') as f:
        await f.write(json.dumps(result_list, ensure_ascii=False, indent=4))
    print(result_list)


# asyncio.run(api_movie())
async def get_api_movie(line, year=2023):
    title = urlencode({"t": line})
    async with httpx.AsyncClient() as client:
        url = f"https://www.omdbapi.com/?i=tt3896198&apikey={settings.movie_api}&{title}&y={year}&plot=full"
        response = await client.get(url)
    return response.json()


async def search_actor_id(name: str = None):
    async with httpx.AsyncClient() as client:
        name = quote(name)
        url = f"https://api.themoviedb.org/3/search/person?query={name}&include_adult=false&language=en-US&page=1"
        headers = {
            "accept": "application/json",
            "Authorization": settings.actor_api
        }
        response = await client.get(url, headers=headers)
        response = response.json()
        if response["total_results"] == 0:
            raise ValueError("Actor not found")
        return response["results"][0]["id"]


async def get_detail_actor_from_api(name: str):
    actor_id = await search_actor_id(name)
    async with httpx.AsyncClient() as client:
        url = f"https://api.themoviedb.org/3/person/{actor_id}?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": settings.actor_api
        }
        response = await client.get(url, headers=headers)
        response = response.json()
        pprint(response)
        return response


# asyncio.run(get_detail_actor_from_api(""))


async def bulk_films():
    file_path = '/home/max-cooper/PycharmProjects/FastAPI-Movies/parser/movie.txt'
    title = []
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
        async for line in f:
            title.append(line)
    print(len(title))
    return title


# asyncio.run(bulk_films())