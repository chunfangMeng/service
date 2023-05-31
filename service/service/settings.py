import os

from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-m4oshs9ichnm86cfl1s$equ41)guof(m!!9s6!o&i8^$r1lr^z'

# DEBUG = False if os.environ.get('ENV') == 'Production' else True
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'captcha',
    'corsheaders',
    'django_filters',
    'django_celery_beat',
    'apps.webapp',
    'apps.member',
    'apps.manager',
    'apps.product'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'libs.runtime_logging.RunTimeMiddleware'
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3000',
    'http://127.0.0.1:3001',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://127.0.0.1:8001'
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-CSRFToken",
    "x-requested-with",
]

CSRF_TRUSTED_ORIGINS = ['http://localhost/', 'http://127.0.0.1/', 'http://localhost:8000/']

ROOT_URLCONF = 'service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'service.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST'),
        'PORT': os.getenv('MYSQL_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('DJANGO_CACHES_LOCATION'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

LANGUAGE_CODE = 'zh-Hans'

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Redis
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
REDIS_DB = int(os.environ.get('REDIS_DB'))

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'drf.pagination.CustomPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    'EXCEPTION_HANDLER': 'drf.exception_handler.custom_exception_handler',
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'drf.throttle.RedisTokenBucketThrottle',
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'redis_token_bucket': '100/hour',
    # },
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

REST_TOKEN_VALID_DAY = os.environ.get('REST_TOKEN_VALID_DAY')

# Captcha
CAPTCHA_IMAGE_SIZE = (80, 45)

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': f"elasticsearch:9200"
    },
}

CUSTOM_PERMISSIONS = (
    ('staff_group', '员工管理'),
    ('staff_view', '员工查看'),
    ('staff_change', '员工编辑'),
    ('staff_remove', '员工删除'),
    ('staff_add', '员工新增'),
    ('shop_brand_group', '商城品牌'),
    ('shop_brand_add', '品牌新增'),
    ('shop_brand_change', '品牌修改'),
    ('shop_brand_delete', '品牌删除'),
    ('shop_brand_view', '品牌查看'),
    ('shop_brand_export', '品牌导出'),
    ('shop_category_group', '商城分类'),
    ('shop_category_view', '商城分类查看'),
    ('shop_category_change', '商城分类修改'),
    ('shop_category_delete', '商城分类删除'),
    ('shop_category_add', '商城分类新增'),
    ('shop_category_export', '商城分类导出'),
    ('shop_attribute_group', '商城属性组'),
    ('shop_attribute_view', '属性组查看'),
    ('shop_attribute_change', '属性组编辑'),
    ('shop_attribute_delete', '属性组删除'),
    ('shop_attribute_export', '属性组导出'),
    ('shop_product_group', '商城商品'),
    ('shop_product_view', '商品查看'),
    ('shop_product_change', '商品编辑'),
    ('shop_product_delete', '商品删除'),
    ('shop_product_add', '商品新增'),
    ('shop_product_export', '商品导出'),
    ('shop_product_attribute_change', '商品属性设置'),
    ('shop_product_specs_change', '商品价格设置'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s] %(message)s'
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} [{message}] {process:d} {thread:d}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'localhost',
            'port': 4560,
            'version': 1,
            'message_type': 'django',
            'fqdn': False,
            'tags': ['django.request'],
        }
    },
    'loggers': {
        '': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'prooagate': True
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'system_watch': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
