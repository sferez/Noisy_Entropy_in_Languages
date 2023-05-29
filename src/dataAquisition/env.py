"""
File inspired from Scweet (https://github.com/Altimis/Scweet.git)
Customized for the purpose of this project
"""

import dotenv
import os
from pathlib import Path

current_dir = Path(__file__).parent.absolute()


def load_env_variable(key, default_value=None, none_allowed=False):
    v = os.getenv(key, default=default_value)
    if v is None and not none_allowed:
        raise RuntimeError(f"{key} returned {v} but this is not allowed!")
    return v


def get_email(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("EMAIL", none_allowed=True)


def get_password(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("PASSWORD", none_allowed=True)


def get_username(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("USERNAME", none_allowed=True)


def get_bearer_token(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("BEARER_TOKEN", none_allowed=True)


def get_chromedriver_path(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("CHROME_DRIVER_PATH", none_allowed=True)
