import pytest
from common.yaml_util import clean_file

@pytest.fixture(scope='session',autouse=True)
def clean_extract():
    clean_file('/config/extract.yml')


