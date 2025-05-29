import os
from celery import Celery

from dotenv import load_dotenv
load_dotenv()

app = Celery('worker')

app.config_from_object({
    'broker_url': os.getenv('BROKER_URL', 'pyamqp://guest:guest@localhost:5672//'),  # Устанавливаем URL для брокера сообщений
    'result_backend': os.getenv('RESULT_BACKEND', 'rpc://'),  # Устанавливаем URL для хранилища результатов
    'timezone': os.getenv('CELERY_TIMEZONE', 'UTC'),  # Таймзона для Celery
    'beat_schedule_filename': os.getenv('CELERY_BEAT_SCHEDULE_FILE', '/Rates-Core/celerybeat-schedule'),  # Файл для хранения расписания beat
})

app.autodiscover_tasks(['worker.tasks', 'core.tasks'])

if __name__ == '__main__':
    app.start()
