from lol_bayes_auth import BayesAuth
import pytest
import requests
from freezegun import freeze_time
import datetime


def test_bayes_auth_init():
    auth = BayesAuth('username', 'password')
    assert auth.username == 'username'
    assert auth.password == 'password'
    assert auth.auth_url == 'https://lolesports-api.bayesesports.com/v2/auth/login'

def test_bayes_auth_init_v1():
    auth = BayesAuth('username', 'password', True)
    assert auth.auth_url == 'https://lolesports-api.bayesesports.com/auth/login'

@freeze_time('2023-01-01 00:00:00')
def test_portal_login(requests_mock):
    auth = BayesAuth('username', 'password')
    # Default expiresIn time of 10 hours
    requests_mock.post(auth.auth_url, json={'accessToken': 'test_token', 'expiresIn': 36000})
    token = auth._portal_login()
    assert token == 'test_token'
    assert auth._token == 'test_token'
    assert auth._expires_at == datetime.datetime(2023, 1, 1, 10, 0)
    
@freeze_time('2023-01-01 00:00:00')
def test_store_token_correctly_stores_all_values():
    auth = BayesAuth('username', 'password')
    response_token = {'accessToken': 'test_token', 'expiresIn': 3600}
    assert auth._token is None
    assert auth._expires_at is None
    token = auth._store_token(response_token)
    assert token == 'test_token'
    assert auth._token == 'test_token'
    assert auth._expires_at == datetime.datetime(2023, 1, 1, 1, 0)  # 1 hour from the frozen time
    
def test_token_refresh_required_requires_refresh_only_when_required(requests_mock):
    with freeze_time('2023-01-01 00:00:00') as frozen_datetime:
        auth = BayesAuth('username', 'password')
        requests_mock.post(auth.auth_url, json={'accessToken': 'test_token', 'expiresIn': 36000})
        auth.get_token()
        
        # Token refresh should not be required
        frozen_datetime.tick(delta=datetime.timedelta(hours=8))
        assert auth._token_refresh_required() == False
        
        # Token should be refreshed after 10 hours
        frozen_datetime.tick(delta=datetime.timedelta(hours=2))
        assert auth._token_refresh_required() == True
        
        # After token refresh, token should not need to be refreshed
        auth.get_token()
        assert auth._token_refresh_required() == False
        
def test_get_token_does_not_call_api_with_fresh_token(requests_mock):
    with freeze_time('2023-01-01 00:00:00') as frozen_datetime:
        auth = BayesAuth('username', 'password')
        requests_mock.post(auth.auth_url, json={'accessToken': 'test_token', 'expiresIn': 36000})
        auth.get_token()
        
        # API should not be called since the token is still valid
        frozen_datetime.tick(delta=datetime.timedelta(hours=8))
        auth.get_token()
        assert requests_mock.call_count == 1
        
        # API should be called since the token is no longer valid
        frozen_datetime.tick(delta=datetime.timedelta(hours=2))
        auth.get_token()
        assert requests_mock.call_count == 2

def test_header_returns_properly_formatted_dictionary(requests_mock):
    auth = BayesAuth('username', 'password')
    requests_mock.post(auth.auth_url, json={'accessToken': 'test_token', 'expiresIn': 36000})
    request_header = auth.get_headers()
    
    assert 'Authorization' in request_header.keys()
    assert request_header.get('Authorization') == 'Bearer test_token'