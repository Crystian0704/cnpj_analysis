from logging import INFO, basicConfig, getLogger
from pathlib import Path
from typing import List, Union

import requests
from bs4 import BeautifulSoup

DATA_DIR = Path(__file__).parent.parent / 'data' / 'raw'
LOG_DIR = Path(__file__).parent.parent / 'logs'
URL = 'https://dadosabertos.rfb.gov.br/CNPJ/'

# create log
basicConfig(
    filename=LOG_DIR / 'cnpj.log',
    level=INFO,
    format='%(asctime)s : %(levelname)s : %(message)s',
)

logger = getLogger(__name__)


def get_link(url: str) -> Union[List[str], None]:

    """Get the link to download the zip file."""

    try:
        request = requests.get(url)
    except requests.exceptions.ConnectionError:
        logger.error('Connection error')
        
        return None

    soup = BeautifulSoup(request.content, 'html.parser')

    # find all link with content zip + url

    find_a = soup.find_all('a', href=True)

    download_link = [
        f"{url}{a['href']}" for a in find_a if a['href'].endswith('.zip')
    ]

    return download_link


def download_zip(download_link: List[str]) -> None:

    """Download the zip file."""

    for link in download_link:

        file_name = link.split('/')[-1]

        logger.info(f'Downloading {file_name}')

        try:
            request = requests.get(link)
        #if connection error or keyboard interrupt break the loop and remove all zip files in data/raw
        except (requests.exceptions.ConnectionError, KeyboardInterrupt):
            logger.error('Connection error')
            logger.info('Removing all zip files in data/raw')
            for file in DATA_DIR.glob('*.zip'):
                file.unlink()
            break

        with open(DATA_DIR / file_name, 'wb') as f:
            f.write(request.content)

        logger.info(f'Downloaded {file_name}')

if __name__ == '__main__':


    download_link = get_link(URL)

    if download_link:
        download_zip(download_link)

    else:
        logger.error('No link to download')

