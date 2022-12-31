from pathlib import Path

from cnpj_project.download_zip import download_zip, get_link

URL = 'https://dadosabertos.rfb.gov.br/CNPJ/'


def test_get_link():

    url = get_link(URL)[0]

    # assert list is not empty
    assert url != [], 'List is empty'
    # assert list is url
    assert url.startswith('http'), 'List is not url'
    # assert list end with zip
    assert url.endswith('.zip'), 'List is not zip'


def test_download_zip():

    url = URL + 'Cnaes.zip'
    download_zip([url])

    # path data/raw

    path = Path(__file__).resolve().parents[2] / 'data' / 'raw'
    # test cnaes.zip is in path

    assert (path / 'Cnaes.zip').exists(), 'File not downloaded'

    # remove file
    (path / 'Cnaes.zip').unlink()
