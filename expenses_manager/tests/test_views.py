from expenses_manager.models import Account, Wallet
from django.db.models.query import QuerySet
import pytest
from django.test.client import Client


@pytest.mark.django_db
@pytest.mark.parametrize('user', [
    {
        'username': 'admin',
        'password': 'helloworld'
    },
    {
        'username': 'jimmy',
        'password': 'helloworldjimmy'
    }
])
def test_login_correct(app: Client, user: dict):
    response = app.post('/expenses-manager/login/', user, follow=True)
    assert response.status_code == 200
    assert response.context['user'].username == user['username']


@pytest.mark.django_db
@pytest.mark.parametrize('user', [
    {
        'username': 'admin',
        'password': '...'
    },
    {
        'username': 'jimmy',
        'password': '...'
    },
    {
        'username': 'adminn',
        'password': 'helloworld'
    },
    {
        'username': 'jimmyy',
        'password': 'helloworldjimmy'
    }
])
def test_login_invalid_credentials(app: Client, user: dict):
    response = app.post('/expenses-manager/login/', user)
    assert response.status_code == 200
    assert 'Invalid credentials' in response.context['form'].non_field_errors()


@pytest.mark.django_db
def test_logout(app: Client):
    app.login(username='admin', password='jelloworld')
    response = app.get('/expenses-manager/logout/', follow=True)
    assert '/expenses-manager/login/' in response.context['request'].path


@pytest.mark.django_db
@pytest.mark.parametrize('user', [
    {
        'username': 'admin',
        'password': 'helloworld'
    },
    {
        'username': 'jimmy',
        'password': 'helloworldjimmy'
    }
])
def test_home_view_available_for_logged_in_user(app: Client, user: dict):
    app.login(username=user['username'], password=user['password'])
    response = app.get('/expenses-manager/home/')
    assert response.status_code == 200
    assert isinstance(response.context['accounts'], QuerySet[Account])


@pytest.mark.django_db
def test_home_view_forbidden_for_not_logged_in(app: Client):
    response = app.get('/expenses-manager/home/', follow=True)
    assert '/expenses-manager/login/' in response.context['request'].path


@pytest.mark.django_db
@pytest.mark.parametrize('user', [
    {
        'username': 'admin',
        'password': 'helloworld',
        'account': {
            'name': 'fooacc',
            'description': '...'
        }
    },
    {
        'username': 'jimmy',
        'password': 'helloworldjimmy',
        'account': {
            'name': 'fooacc'
        }
    }
])
def test_create_account(app: Client, user: dict):
    app.login(username=user['username'], password=user['password'])
    response = app.post('/expenses-manager/create-account/', user['account'], follow=True)
    assert response.status_code == 200
    assert isinstance(response.context['accounts'], QuerySet[Account])
    assert len(response.context['accounts']) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('user', [
    {
        'username': 'admin',
        'password': 'helloworld',
        'account': {
            'name': 'fooacc',
            'description': '...'
        }
    },
    {
        'username': 'jimmy',
        'password': 'helloworldjimmy',
        'account': {
            'name': 'fooacc'
        }
    }
])
def test_account_details(app: Client, user: dict):
    app.login(username=user['username'], password=user['password'])
    r = app.post('/expenses-manager/create-account/', user['account'], follow=True)
    acc_pk = r.context['accounts'][0].pk
    response = app.get(f'/expenses-manager/accounts/{acc_pk}/')
    assert response.status_code == 200
    assert isinstance(response.context['account'], Account)


@pytest.mark.django_db
@pytest.mark.parametrize('user', [
    {
        'username': 'admin',
        'password': 'helloworld',
        'account': {
            'name': 'foo'
        },
        'wallet': {
            'name': 'wally',
        }
    },
    {
        'username': 'jimmy',
        'password': 'helloworldjimmy',
        'account': {
            'name': 'bar'
        },
        'wallet': {
            'name': 'willy',
        }
    }
])
def test_create_wallet_and_wallet_details(app: Client, user: dict):
    app.login(username=user['username'], password=user['password'])
    r = app.post('/expenses-manager/create-account/', user['account'], follow=True)
    acc_pk = r.context['accounts'][0].pk
    response = app.post(f'/expenses-manager/accounts/{acc_pk}/create-wallet/', user['wallet'], follow=True)
    assert response.status_code == 200
    assert isinstance(response.context['wallet'], Wallet)


@pytest.mark.django_db
@pytest.mark.parametrize('user', [
    {
        'username': 'admin',
        'password': 'helloworld',
        'account': {
            'name': 'foo'
        },
        'wallet': {
            'name': 'wally',
        }
    },
    {
        'username': 'jimmy',
        'password': 'helloworldjimmy',
        'account': {
            'name': 'bar'
        },
        'wallet': {
            'name': 'willy',
        }
    }
])
def test_create_expense(app: Client, user: dict):
    app.login(username=user['username'], password=user['password'])
    r = app.post('/expenses-manager/create-account/', user['account'], follow=True)
    acc_pk = r.context['accounts'][0].pk
    rr = app.post(f'/expenses-manager/accounts/{acc_pk}/create-wallet/', user['wallet'], follow=True)
    wallet_pk = rr.context['wallet'].pk
    expense = {
        'pin': True,
        'category': 1,
        'name': 'ipad',
        'amount': 1000.22
    }
    response = app.post(f'/expenses-manager/accounts/{acc_pk}/wallets/{wallet_pk}/create-expense/', expense, follow=True)
    assert response.status_code == 200
    assert isinstance(response.context['wallet'], Wallet)


@pytest.mark.django_db
@pytest.mark.parametrize('user', [
    {
        'username': 'admin',
        'password': 'helloworld',
        'account': {
            'name': 'foo'
        },
        'wallet': {
            'name': 'wally',
        }
    },
    {
        'username': 'jimmy',
        'password': 'helloworldjimmy',
        'account': {
            'name': 'bar'
        },
        'wallet': {
            'name': 'willy',
        }
    }
])
def test_create_delete_expense(app: Client, user: dict):
    app.login(username=user['username'], password=user['password'])
    r = app.post('/expenses-manager/create-account/', user['account'], follow=True)
    acc_pk = r.context['accounts'][0].pk
    rr = app.post(f'/expenses-manager/accounts/{acc_pk}/create-wallet/', user['wallet'], follow=True)
    wallet_pk = rr.context['wallet'].pk
    expense = {
        'pin': True,
        'category': 1,
        'name': 'ipad',
        'amount': 1000.22
    }
    rrr = app.post(f'/expenses-manager/accounts/{acc_pk}/wallets/{wallet_pk}/create-expense/', expense, follow=True)
    expense_pk = rrr.context['expenses'][0].pk
    before_count = len(rrr.context['expenses'])
    response = app.post(f'/expenses-manager/accounts/{acc_pk}/wallets/{wallet_pk}/delete-expense/{expense_pk}/', {'expense_pk': expense_pk}, follow=True)
    assert response.status_code == 200
    after_count = len(response.context['expenses'])
    assert after_count == (before_count - 1)
