import os
from datetime import timedelta
from celery import Celery

from dotenv import load_dotenv
load_dotenv()

app = Celery('core')

app.config_from_object({
    'broker_url': os.getenv('BROKER_URL', 'pyamqp://guest:guest@localhost:5672//'),
    'result_backend': os.getenv('RESULT_BACKEND', 'rpc://'),
    'timezone': os.getenv('CELERY_TIMEZONE', 'UTC'),
    'beat_schedule_filename': os.getenv('CELERY_BEAT_SCHEDULE_FILE', '/Rates-Core/celerybeat-schedule'),
})

app.conf.beat_schedule = {
    'fetch_config_and_send_to_worker_every_5_minutes': {
        'task': 'core.tasks.fetch_config_and_send_to_worker',
        'schedule': timedelta(seconds=30),
    },
    'export_data_and_send_to_email_daily': {
        'task': 'core.tasks.export_data_and_send_to_email',
        'schedule': timedelta(seconds=60),
    },
}
app.autodiscover_tasks(['worker.tasks', 'core.tasks'])

if __name__ == '__main__':
    app.start()
