import os
from decouple import config, Config, RepositoryEnv


class Conf:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.env = config
        self.secrets = Config(RepositoryEnv(
            self.env("APP_SECRETS_FILE")))

    def influx_token(self):
        with open(self.env("INFLUX_TOKEN_FILE"), "r") as file:
            return file.read().strip()
