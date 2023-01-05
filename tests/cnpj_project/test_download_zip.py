from pathlib import Path

from cnpj_project.download_zip import download_zip, get_link

URL = 'https://dadosabertos.rfb.gov.br/CNPJ/'


def test_get_link():

    """Testa se não está vazia e se começa com http e termina com zip.

    params: None
    return: None

    """

    url = get_link(URL)[0]   # type: ignore

    # garante que a lista não está vazia
    assert url != [], 'List is empty'
    # garante que a lista começa com http
    assert url.startswith('http'), 'List is not url'
    # garante que a lista termina com zip
    assert url.endswith('.zip'), 'List is not zip'


def test_download_zip():

    """Testa se o arquivo foi baixado e se foi removido.

    params: None
    return: None

    """

    url = URL + 'Cnaes.zip'
    download_zip([url])

    # ajusta caminho data/raw
    path = Path(__file__).resolve().parents[2] / 'data' / 'raw'

    # garante que o arquivo foi baixado
    assert (path / 'Cnaes.zip').exists(), 'File not downloaded'

    # remove o arquivo baixado
    (path / 'Cnaes.zip').unlink()
