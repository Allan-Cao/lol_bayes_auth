# Based on example implementation from Bayes Esports API documentation (https://docs.bayesesports.com/docs-data-portal/api/token_reuse)

import requests
from datetime import datetime, timedelta


class BayesAuth:
    def __init__(self, username: str, password: str, v1_auth: bool = False):
        self.username = username
        self.password = password
        self.auth_url = (
            "https://lolesports-api.bayesesports.com/auth/login"
            if v1_auth
            else "https://lolesports-api.bayesesports.com/v2/auth/login"
        )
        self._token = None
        self._expires_at = None

    def _portal_login(self) -> str:
        """Login to the Bayes API and store the access token in a JSON file. If the token is already stored and is still valid, it will be used instead of sending a new request to the API.

        :return: Bayes API access token
        :rtype: str
        """
        headers = {"Content-Type": "application/json"}
        creds = {"username": self.username, "password": self.password}
        response = requests.post(self.auth_url, json=creds, headers=headers)
        if response.ok:
            return self._store_token(response.json())
        else:
            response.raise_for_status()

    def _store_token(self, response_token: dict) -> str:
        """Save access token and time to expiration with a datetime object.

        :param response_token: Bayes API response
        :type response_token: dict
        :return: Bayes API access token
        :rtype: str
        """
        self._token = response_token["accessToken"]
        self._expires_at = datetime.now() + timedelta(
            seconds=response_token["expiresIn"]
        )
        return self._token

    def _token_refresh_required(self) -> bool:
        """Check if the access token that is stored is still valid

        :return: True if the token is still valid, False otherwise
        :rtype: bool
        """
        if self._expires_at is None:
            raise ValueError("No token has been stored yet.")
        return datetime.now() >= self._expires_at

    def get_token(self) -> str:
        """Get the Bayes API access token. If the token is already stored and is still valid, it will be used instead of sending a new request to the API.

        :return: Bayes API access token
        :rtype: str
        """
        if self._token is None or self._token_refresh_required():
            return self._portal_login()
        return self._token
