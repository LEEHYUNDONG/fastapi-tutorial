from dataclasses import dataclass ,asdict
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    """기본 configuration"""

    BASE_DIR = base_dir

    DB_POOL_RECYCLE : int = 900
    DB_ECHO:bool = True
    DB_URL : str = "mysql+pymysql://root:1234@localhost:3306/fastapitutorial?charset=utf8mb4"

@dataclass
class LocalConfig(Config):
    PROJ_RELOAD:bool = True
    

@dataclass
class ProdConfig(Config):
    PROJ_RELOAD:bool = False

def conf():
    """환경 불러오기"""
    # print(asdict(LocalConfig())) # dictionary로 변경 가능
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))
