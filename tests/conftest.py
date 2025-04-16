from typing import NoReturn

import faker
import pytest


@pytest.fixture(scope='session')
def fake():
    return faker.Faker()


@pytest.fixture(autouse=True)
def ban_external_requests(monkeypatch) -> NoReturn:
    """Ban on any external requests."""
    m_path = 'urllib3.connectionpool.HTTPConnectionPool.urlopen'

    def _ban_external_requests(http_connection_pool, **_):
        msg = 'Attempting to make a request to `{host}` without a mock'
        raise RuntimeError(
            msg.format(
                host=http_connection_pool.host,
            )
        )

    monkeypatch.setattr(
        m_path,
        _ban_external_requests,
    )
