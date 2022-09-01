from environs import Env
from sanic_envconfig import EnvConfig

env = Env()
env.read_env()


class Settings(EnvConfig):
    DEBUG = True
    HOST = env.str("HOST")
    PORT = env.int("PORT")
