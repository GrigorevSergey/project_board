from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Отключаем cachalot для тестов
CACHALOT_ENABLED = False

# Настраиваем django-ratelimit для использования локального кэша
RATELIMIT_CACHE_BACKEND = "default"
