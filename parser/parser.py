import json
from urllib.parse import urlencode

import httpx
from bs4 import BeautifulSoup


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
    with open("movie.txt", mode='r', encoding='utf-8') as f:
        for line in f:
            title = urlencode({"t": line})
            list_movie.append(title)
    async with httpx.AsyncClient() as client:
        for movie in list_movie:
            url = f"https://www.omdbapi.com/?i=tt3896198&apikey=16fe9e89&{movie}&y=2023&plot=full"
            response = await client.get(url)
            result_list.append(response.json())
    with open("result_movie.json", "w", encoding='utf-8') as f:
        json.dump(result_list, f, ensure_ascii=False, indent=4)
    print(result_list)


# asyncio.run(api_movie())
async def get_api_movie(line, year=2023):
    title = urlencode({"t": line})
    async with httpx.AsyncClient() as client:
        url = f"https://www.omdbapi.com/?i=tt3896198&apikey=16fe9e89&{title}&y={year}&plot=full"
        response = await client.get(url)
    return response.json()
