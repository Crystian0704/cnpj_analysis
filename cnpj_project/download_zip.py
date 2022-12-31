from logging import INFO, basicConfig, getLogger
from pathlib import Path

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


def get_data(url: str) -> list:

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


def download_zip(urls) -> None:
    
        for url in urls:
            try:
                request = requests.get(url)
            except requests.exceptions.ConnectionError:
                logger.error('Connection error')
                continue
    
            file_name = url.split('/')[-1]
    
            with open(DATA_DIR / file_name, 'wb') as f:
                f.write(request.content)
    
            logger.info(f'Download {file_name} completed')


if __name__ == '__main__':
    
    urls = get_data(URL)
    download_zip(urls)
