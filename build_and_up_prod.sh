#! /bin/bash
cat > service/.env.prod << EOF
ENV=Production  # Develop or Production

CELERY_BACKEND=redis://redis:6379/3
CELERY_BROKER=redis://redis:6379/3
DJANGO_CACHES_LOCATION=redis://redis:6379/1

MYSQL_ROOT_PASSWORD=123456
MYSQL_USER=dbuser
MYSQL_DATABASE=service_db
MYSQL_PASSWORD=password
MYSQL_HOST=db
MYSQL_PORT=3306

REST_TOKEN_VALID_DAY = 7

# REDIS
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=2

# ELASTICSEARCH
ELASTICSEARCH_HOST=elasticsearch

# LOGSTASH
LOGSTASH_HOST=logstash
EOF

docker-compose up -d --build
