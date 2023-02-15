"""Baixa o arquivo zip do site da Receita Federal."""

from logging import INFO, basicConfig, getLogger
from pathlib import Path
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

# ajusta os caminhos das pastas
DATA_DIR = Path(__file__).parent.parent / 'data' / 'raw'
LOG_DIR = Path(__file__).parent.parent / 'logs'
URL = 'https://dadosabertos.rfb.gov.br/CNPJ/'

# cria a configuração do log e o logger
basicConfig(
    filename=LOG_DIR / 'cnpj.log',
    level=INFO,
    format='%(asctime)s : %(levelname)s : %(message)s',
)

logger = getLogger(__name__)


def get_link(url: str) -> Optional[List[str]]:
    """Obtém o link para baixar o arquivo zip.

    Args:
        url (str): url para obter o link

    Returns:
        list: lista de links de download ou None em caso de falha na conexão
    """
    try:
        request = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        logger.error('Erro de conexão')

        return None

    soup = BeautifulSoup(request.content, 'html.parser')

    # encontra todos os links com o conteúdo zip + url
    find_a = soup.find_all('a', href=True)

    download_link = [
        f"{url}{a['href']}" for a in find_a if a['href'].endswith('.zip')
    ]

    return download_link


def download_zip(download_link: List[str]) -> None:
    """Baixa o arquivo zip.

    Args:
        download_link (list): lista de links de download

    Returns:
        None
    """
    for link in download_link:

        file_name = link.split('/')[-1]
        # Use lazy % formatting in logging functions
        logger.info('Baixando arquivo %s', file_name)

        try:
            request = requests.get(link, timeout=5)
        except (requests.exceptions.ConnectionError, KeyboardInterrupt):
            logger.error('Erro de conexão')
            logger.info('Removendo todos os arquivos zip em data/raw')
            for file in DATA_DIR.glob('*.zip'):
                # se houver erro, remove o arquivo
                file.unlink()
            break

        with open(DATA_DIR / file_name, 'wb') as filename:
            filename.write(request.content)


if __name__ == '__main__':

    download = get_link(URL)

    if download:
        download_zip(download)

    else:
        logger.error('Nenhum link para baixar encontrado!')
