from dotenv import find_dotenv, dotenv_values


env_path = find_dotenv()

config = dotenv_values(env_path)


class Config:
    SECRET_KEY: str = config['SECRET_KEY']
    ALGORITHM: str = config['ALGORITHM']
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config["ACCESS_TOKEN_EXPIRE_MINUTES"]
    ALLOWED_FRONTEND_URL: str = config['ALLOWED_FRONTEND_URL']



   