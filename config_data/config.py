from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


env = Env()
env.read_env()


def load_config() -> Config:
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))


PAGE_SIZE = 1050
