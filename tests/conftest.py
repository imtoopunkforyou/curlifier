import faker
import pytest


@pytest.fixture(scope='session')
def fake():
    return faker.Faker()
