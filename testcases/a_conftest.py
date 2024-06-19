# -*- coding: UTF-8 -*-
import pytest
import requests


@pytest.fixture(scope='session')
def get_session():
    session = requests.session()    # 获得session会话对象
    return session





