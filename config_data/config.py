from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


env = Env()


def load_config(path: str | None = None) -> Config:
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))


PAGE_SIZE = 1050
