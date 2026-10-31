import os
from dotenv import load_dotenv

load_dotenv()


class Setting:
    model_name: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


setting = Setting()