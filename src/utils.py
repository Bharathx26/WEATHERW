from dotenv import load_dotenv

def load_env(env_path: str = ".env"):
    """
    Load environment variables from .env if present.
    """
    load_dotenv(env_path)
