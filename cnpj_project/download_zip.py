import asyncio
from logging import INFO, basicConfig, getLogger
from pathlib import Path

import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
LOG_DIR = Path(__file__).parent.parent / "logs"

# create log
basicConfig(
    filename=LOG_DIR / "cnpj.log",
    level=INFO,
    format="%(asctime)s : %(levelname)s : %(message)s",
)


def get_data():
    url = "https://dadosabertos.rfb.gov.br/CNPJ/"
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, "html.parser")
        getLogger().info("Requisição feita com sucesso")
    except:
        getLogger().error("Erro na requisição")
    
    # find all link with content zip + url
    download_link = [
        a.get("href") for a in soup.find_all("a") if a.get("href").find(".zip") > 0
    ]
    return [url + link for link in download_link]


# async downloading zip a list of urls using aiohttp and aiofiles


def download_zip(url):
    sema = asyncio.Semaphore(3)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    async def download(url, session):
        async with sema:
            async with session.get(url) as response:
                filename = url.split("/")[-1]
                async with aiofiles.open(DATA_DIR / filename, "wb") as f:
                    await f.write(await response.read())

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(download(url, session)) for url in url]
            await asyncio.gather(*tasks)

    try:
        asyncio.run(main())
    except TimeoutError:
        # remove raw dir
        Path(DATA_DIR).rmdir()


if __name__ == "__main__":
    url = get_data()
    download_zip(url)
