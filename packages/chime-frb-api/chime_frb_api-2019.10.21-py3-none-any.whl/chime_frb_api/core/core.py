#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Core API Class Object
"""
from os import environ
from getpass import getpass
import requests
import logging
import typing as t


JSON = t.Union[str, int, float, bool, None, t.Mapping[str, "JSON"], t.List["JSON"]]

# Logging Config
LOGGING_CONFIG = {}
logging_format = "[%(asctime)s] %(levelname)s "
logging_format += "%(module)s::%(funcName)s(): "
logging_format += "%(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO)
log = logging.getLogger()


class APIError(Exception):
    """
    CHIME/FRB API Error
    """


class ConfigurationError(APIError):
    """
    Configuration error ocurred
    """


class TokenError(APIError):
    """
    Error with CHIME/FRB Tokens
    """


class API(object):
    """
    Application Programming Interface Base Class
    """

    def __init__(self, **kwargs):
        """
         CHIME/FRB Core API Initialization

        Parameters
        ----------
        **kwargs: dict

        base_url : str
            Base URL for CHIME/FRB Master
        access_token : str
            Access token for authentiation
        refresh_token : str
            Refresh token to authentiation
        username : str
            CHIME username
        password : str
            CHIME password

        Returns
        -------
        class-type

        Raises
        ------
        APIError
            CHIME/FRB API Error Ocurred
        """
        # Create a requests session
        self._session = requests.Session()

        # Base url for CHIME/FRB Master
        self.base_url = kwargs.get("base_url", None)

        # Collect authentiation parameters if they were initialized
        self.access_token = kwargs.get("access_token", None)
        self.refresh_token = kwargs.get("refresh_token", None)
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)

        # Get configuration parameters from env
        self._config_from_env()

        # Basic Configuration Checks
        self._check_configuration()

    def _config_from_env(self, environment: dict = None) -> None:
        if not environment:
            environment = environ
        if not self.access_token:
            self.access_token = environ.get("FRB_MASTER_ACCESS_TOKEN", None)
        if not self.refresh_token:
            self.refresh_token = environ.get("FRB_MASTER_REFRESH_TOKEN", None)
        if not self.base_url:
            self.base_url = environ.get("FRB_MASTER_BASE_URL", None)
        if not self.username:
            self.username = environ.get("FRB_MASTER_USERNAME", None)
        if not self.password:
            self.password = environ.get("FRB_MASTER_PASSWORD", None)

    def _check_configuration(self):
        if not self.base_url:
            raise ConfigurationError("base_url not configured")

    def _coalesse_parameters(
        self,
        access_token: str = None,
        refresh_token: str = None,
        username: str = None,
        password: str = None,
    ):
        # Gather authentication parameters if none were provided
        if not access_token:
            access_token = self.access_token
        if not refresh_token:
            refresh_token = self.refresh_token
        if not username:
            username = self.username
        if not password:
            password = self.password
        return access_token, refresh_token, username, password

    def _get_user_details(self, username: str = None, password: str = None):
        if not username:
            username = input("Username: ")
            # Save username for future uses
            self.username = username
        if not password:
            # Get the password if we don't have it
            password = getpass("Password: ")
        return username, password

    def authorize(
        self,
        access_token: str = None,
        refresh_token: str = None,
        username: str = None,
        password: str = None,
    ) -> bool:
        access_token, refresh_token, username, password = self._coalesse_parameters(
            access_token, refresh_token, username, password
        )
        try:
            # We already have access_token, check if it is valid
            if access_token:
                log.info("Authorization Method: access_token")
                self._session.headers.update(authorization=access_token)
                response = self._session.get(self.base_url + "/auth/verify")
                response.raise_for_status
                # Tokens are good, return True
                if response.json().get("valid", False):
                    log.info("Authorization Result: passed")
                    self.access_token = access_token
                    self.refresh_token = refresh_token
                    return True
                else:
                    log.info("token authorization: failed")
                    self._session.headers.pop("authorization", None)

            # If token authentiation was not successful try user/pass
            log.info("Authorization Method: User/Pass")
            username, password = self._get_user_details(
                username=username, password=password
            )
            payload = {}
            payload.update(username=username, password=password)
            response = self._session.post(url=self.base_url + "/auth", json=payload)
            response.raise_for_status()
            log.info("Authorization Result: passed")
            tokens = response.json()
            log.debug(tokens)
            self.username = username
            self.access_token = tokens.get("access_token", None)
            self.refresh_token = tokens.get("refresh_token", None)
            self._session.headers.update(authorization=self.access_token)
            return True
        except requests.exceptions.RequestException as e:
            log.info("Authorization Result: failed")
            self._session.headers.pop("authorization", None)
            log.error(response.text)
            raise e

    def reauthorize(self, access_token: str = None, refresh_token: str = None) -> bool:
        access_token, refresh_token, username, password = self._coalesse_parameters(
            access_token, refresh_token
        )
        try:
            if not (refresh_token or access_token):
                raise TokenError("missing refresh or access token")
            log.info("Re-authorizing Method: tokens")
            self._session.headers.update(authorization=access_token)
            payload = {}
            payload.update(refresh_token=refresh_token)
            response = self._session.post(self.base_url + "/auth/refresh", json=payload)
            response.raise_for_status()
            tokens = response.json()
            log.debug(tokens)
            self.access_token = tokens.get("access_token", None)
            self.refresh_token = refresh_token
            log.info("Re-authorizing Result: passed")
            return True
        except requests.exceptions.RequestException as e:
            log.info("Re-authorizing Result: failed")
            log.error(response.text)
            raise e

    ###########################################################################

    def post(self, url: str, **kwargs) -> JSON:
        """
        HTTP Post

        Parameters
        ----------
        url : str
            HTTP URL
        **kwargs : dict
            Keyworded arguments, synonmous to requests.post

        Returns
        -------
        response : json

        Raises
        ------
        requests.exceptions.RequestException
        """
        try:
            response = self._session.post(self.base_url + url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e

    def patch(self, url: str, **kwargs) -> JSON:
        try:
            response = self._session.patch(self.base_url + url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e

    def get(self, url: str, **kwargs) -> JSON:
        try:
            response = self._session.get(self.base_url + url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e

    def delete(self, url: str, **kwargs) -> JSON:
        try:
            response = self._session.delete(self.base_url + url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise e

    def put(self, url: str, **kwargs) -> JSON:
        try:
            response = self._session.put(self.base_url + url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e
