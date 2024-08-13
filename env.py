import os
import functools
from typing import Callable, overload
import sqlalchemy.engine.url
from dotenv import dotenv_values
from pathlib import Path

env_file_values = dotenv_values(
    os.environ.get("ENV_FILE_PATH", str(Path.cwd() / ".env"))
)

def _get_env_var[
    T
](key: str, default: str | None = None, *, coerce: Callable[[str], T],) -> T:
    str_value = os.environ.get(key, None)
    if str_value is None:
        str_value = env_file_values.get(key, None)

    if str_value is None:
        if default is None:
            raise MissingEnvVarError(key)
        else:
            str_value = default

    try:
        return coerce(str_value)
    except (ValueError, TypeError) as e:
        raise InvalidEnvVarError(key, str_value) from e


@functools.lru_cache(1)
def database_connection_string() -> str:
    def coerce_connection_string(db_url: str):
        try:
            sqlalchemy.engine.url.make_url(db_url)
        except Exception as e:
            raise InvalidEnvVarError("DATABASE_CONNECTION_STRING", db_url) from e
        return db_url

    return _get_env_var("DATABASE_CONNECTION_STRING", coerce=coerce_connection_string)


def database_pool_size() -> int:
    # See https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.pool_size
    return _get_env_var("DATABASE_POOL_SIZE", default="5", coerce=int)

def database_max_overflow() -> int:
    # See https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.max_overflow
    return _get_env_var("DATABASE_MAX_OVERFLOW", default="10", coerce=int)

def database_pool_timeout() -> int:
    # See https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.timeout
    return _get_env_var("DATABASE_POOL_TIMEOUT", default="30", coerce=int)

def _surround_with_quotes(string: str) -> str:
    if "'" not in string:
        return f"'{string}'"

    if '"' not in string:
        return f'"{string}"'

    if "'''" not in string:
        return f"'''{string}'''"

    return f'"""{string}"""'


class MissingEnvVarError(ValueError):
    def __init__(self, env_var_name: str) -> None:
        self.env_var_name = env_var_name
        self.message = (
            f"Missing environment variable: {_surround_with_quotes(env_var_name)}"
        )

        super().__init__(self.message)


class InvalidEnvVarError(ValueError):
    def __init__(self, env_var_name: str, env_var_value: str) -> None:
        self.env_var_name = env_var_name
        self.env_var_value = env_var_value
        self.message = f"Invalid environment variable: {_surround_with_quotes(env_var_name)} = {_surround_with_quotes(env_var_value)}"

        super().__init__(self.message)
