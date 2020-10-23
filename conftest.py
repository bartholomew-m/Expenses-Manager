import pytest
from django.test import Client
from djangoproject import settings
from django.core.management import call_command


def pytest_configure():
    settings.DATABASES = {
        'default': {
            'ENGINE':'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test-data.json')


@pytest.fixture(scope='session')
def app(django_db_setup):
    return Client()
