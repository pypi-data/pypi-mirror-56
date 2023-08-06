==========
Openauth
==========

Openauth 是 统一认证平台的 django 插件。

通过这个插件，django 可以与 统一认证平台 集成起来，直接具备如 企业微信 登录能力。

原理上，就是直接改写 django admin 的 login 页，使其接受 jwt 参数，判断 jwt 合法性，从中解析用户账号。
如果账号存在，则直接登录，如果不存在，则创建后再置为登录态。

其中统一认证平台可以自己搭建。

Quick start
--------------

1. 安装 ::

    pip install django-openauth

2. 在 settings 加入 uniauth ::

    INSTALLED_APPS = [
        ...
        'openauth',
    ]

3. 在 urls.py 加入 openauth ::

    path('openauth/', include('openauth.urls')),

4. 同步数据库 ::

    python manage.py migrate

5. 访问 http://localhost:8000/admin 看效果

配置项
----------

* settings 支持以下配置项:

  * OPENAUTH_JWT_SECRET：如果该配置项有值，或值不为空字符串，则 jwt 的认证 secret 从该项获取。
    这时不需要 redis。若该配置项为空，则 openauth 会从 Redis 中的 jwt_secret 中获取 secret

* 如果 jwt secret 从 redis 中获取，请在 settings 的 cache 中这么配置::

     CACHES = {
        'default': {
            ...
        },
        'openauth': {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"redis://{config.openauth_redis_host}:{config.openauth_redis_port}/{config.openauth_redis_db}",
            'KEY_PREFIX': '',
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": f"{config.openauth_redis_password}"
            }
        }
     }



