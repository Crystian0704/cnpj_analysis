import pytest
from cnpj_project.download_zip import get_data, download_zip
from pathlib import Path

def test_get_data():
    #assert list is not empty
    assert get_data() != [], "List is empty"
    #assert list is url
    assert get_data()[0].startswith('http'), "List is not url"
    #assert list end with zip
    assert get_data()[0].endswith('.zip'), "List is not zip"


