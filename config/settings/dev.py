from .common import *
import environ
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = 'django-insecure-nb+6d+80=r_e0(z^$kys@n@i1%c@iyag6%*47b@f37%$dyy_1z'
DEBUG = True


ALLOWED_HOSTS = ["localhost", "127.0.0.1","0.0.0.0"]



env = environ.Env(
    DEBUG=(bool, True),
    DB_PORT=(int, 5432),
)

environ.Env.read_env(os.path.join(BASE_DIR, "backend.env"))


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
      
    }
}

