from enum import Enum

from art import text2art

from utils.exceptions import SystemExitException


class EnvironmentDto:
    name: str


class Environments(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    LOCALHOST = "localhost"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class EnvironmentService:
    __environment__: Environments = None

    def __init__(self, environment: Environments):
        self.environment: Environments = environment

    @property
    def environment(self):
        return EnvironmentService.__environment__

    @environment.setter
    def environment(self, environment: Environments):
        if EnvironmentService.__environment__ is None:
            if environment.value in Environments.list():
                EnvironmentService.__environment__ = environment
                wx_environment = text2art(
                    EnvironmentService.__environment__.value.upper(),
                    font="starwars",
                    chr_ignore=True,
                )
                print(wx_environment)
            else:
                raise SystemExitException(message="Environment Not Defined!")
        else:
            raise SystemExitException(message="Environment Already Defined!")
