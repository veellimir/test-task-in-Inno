import os

from dotenv import load_dotenv

load_dotenv()

ENV__SECRET_KEY = os.getenv("SECRET_KEY")
ENV__DEBUG = os.getenv("DEBUG")
ENV__ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")