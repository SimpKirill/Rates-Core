# Rates-Core

#### Requirements

```.env
- Python 3.8+
- PostgreSQL
```

#### How to build
#### Docker
- Create .env file, for example
```
BROKER_URL=pyamqp://guest:guest@rabbitmq:5672//
DB_URL=postgresql://user:password@postgres:5432/rates_db

POSTGRES_HOST=postgres
POSTGRES_USER="<YOUR DATABASE USER>"
POSTGRES_PASSWORD="<YOUR DATABASE USER PASSWORD>"
POSTGRES_DB="<YOUR DATABASE NAME>"
POSTGRES_PORT=5432
POSTGRES_EXTERNAL_PORT=5433

RABBITMQ_HOST=rabbitmq
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_PORT=5672

CELERY_BROKER_URL=amqp://$RABBITMQ_USER:$RABBITMQ_PASSWORD@$RABBITMQ_HOST:$RABBITMQ_PORT//
CELERY_RESULT_BACKEND=rpc://

TIMEZONE=UTC

# TLS SMTP
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_USER=
EMAIL_SMTP_PASSWORD=

```
- Build Docker container
```
docker-compose up --build
```