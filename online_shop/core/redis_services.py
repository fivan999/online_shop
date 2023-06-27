import redis

import django.conf


# подключение к базе данных Redis
redis_connection = redis.Redis(
    host=django.conf.settings.REDIS_HOST,
    port=django.conf.settings.REDIS_PORT,
    db=django.conf.settings.REDIS_DB,
)
