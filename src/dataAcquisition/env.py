"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:credits: Scweet: An extensive toolbox to scrape Twitter, written in Python.
:description: Load environment variables.
"""


# -------------------------------------------- IMPORTS --------------------------------------------------------------- #

# External
import dotenv
import os
from pathlib import Path


# -------------------------------------------- FUNCTIONS ------------------------------------------------------------- #

current_dir = Path(__file__).parent.absolute()


def load_env_variable(key, default_value=None, none_allowed=False):
    """
    Load an environment variable

    :param key: key of the environment variable
    :type key: str
    :param default_value: default value if the environment variable is not found
    :type default_value: str
    :param none_allowed: if the environment variable can be None
    :type none_allowed: bool
    :return: value of the environment variable
    :rtype: str

    >>> load_env_variable("TEST", default_value="test")
    >>> 'test'
    """
    v = os.getenv(key, default=default_value)
    if v is None and not none_allowed:
        raise RuntimeError(f"{key} returned {v} but this is not allowed!")
    return v


def get_email(env):
    """
    Get the email from the environment variables

    :param env: path to the .env file
    :type env: str
    :return: email
    :rtype: str

    >>> get_email(".env")
    """
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("EMAIL", none_allowed=True)


def get_password(env):
    """
    Get the password from the environment variables

    :param env: path to the .env file
    :type env: str
    :return: password
    :rtype: str

    >>> get_password(".env")
    """
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("PASSWORD", none_allowed=True)


def get_username(env):
    """
    Get the username from the environment variables

    :param env: path to the .env file
    :type env: str
    :return: username
    :rtype: str

    >>> get_username(".env")
    """
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("USERNAME", none_allowed=True)


def get_consumer_key(env):
    """
    Get the consumer key from the environment variables

    :param env: path to the .env file
    :type env: str
    :return: consumer key
    :rtype: str

    >>> get_consumer_key(".env")
    """
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("CONSUMER_KEY", none_allowed=True)


def get_consumer_secret(env):
    """
    Get the consumer secret from the environment variables

    :param env: path to the .env file
    :type env: str
    :return: consumer secret
    :rtype: str

    >>> get_consumer_secret(".env")
    """
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("CONSUMER_SECRET", none_allowed=True)


def get_access_token(env):
    """
    Get the access token from the environment variables

    :param env: path to the .env file
    :type env: str
    :return: access token
    :rtype: str

    >>> get_access_token(".env")
    """
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("ACCESS_TOKEN", none_allowed=True)


def get_access_token_secret(env):
    """
    Get the access token secret from the environment variables

    :param env: path to the .env file
    :type env: str
    :return: access token secret
    :rtype: str

    >>> get_access_token_secret(".env")
    """
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("ACCESS_TOKEN_SECRET", none_allowed=True)


def get_bearer_token(env):
    """
    Get the bearer token from the environment variables

    :param env: path to the .env file
    :type env: str
    :return: bearer token
    :rtype: str

    >>> get_bearer_token(".env")
    """
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("BEARER_TOKEN", none_allowed=True)


def get_chromedriver_path(env):
    """
    Get the chromedriver path from the environment variables

    :param env: path to the .env file
    :type env: str
    :return: chromedriver path
    :rtype: str

    >>> get_chromedriver_path(".env")
    """
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("CHROME_DRIVER_PATH", none_allowed=True)
