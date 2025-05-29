from core.celery import app
from core.models import Session, Config, Currency
from core.logger import setup_logger
import json

logger = setup_logger("tasks")


@app.task
def fetch_config_and_send_to_worker():
    logger.info("Запуск задачи: fetch_config_and_send_to_worker")
    session = Session()
    configs = session.query(Config).filter(Config.step == 1).all()
    logger.info(f"Найдено конфигураций для step=1: {len(configs)}")

    for config in configs:
        logger.info(f"Отправка задачи для валюты: {config.currency_code}, дата: {config.date}")
        app.send_task("worker.tasks.fetch_rates_from_api", args=[config.currency_code, str(config.date)])

    session.close()
    logger.info("Завершена задача: fetch_config_and_send_to_worker")


@app.task
def save_rates(data):
    logger.info("Получены данные для сохранения в rates")
    session = Session()
    rate_data = json.loads(data)

    currency_code = rate_data.get("currency_code")
    currency_date = rate_data.get("currency_date")

    existing_rate = session.query(Currency).filter_by(
        currency_code=currency_code,
        currency_date=currency_date
    ).first()

    if existing_rate:
        for key, value in rate_data.items():
            setattr(existing_rate, key, value)
        session.commit()
        logger.info(f"Обновлён курс валюты: {currency_code} на дату {currency_date}")
    else:
        rate = Currency(**rate_data)
        session.add(rate)
        session.commit()
        logger.info(f"Сохранён новый курс валюты: {currency_code} на дату {currency_date}")

    session.close()


@app.task
def export_data_and_send_to_email():
    logger.info("Запуск задачи: export_data_and_send_to_email")
    session = Session()
    configs = session.query(Config).filter(Config.step == 2).all()
    export_list = []

    for config in configs:
        logger.info(f"Обработка экспорта для валюты: {config.currency_code}, дата: {config.date}")
        rates = session.query(Currency).filter(
            Currency.currency_code == config.currency_code,
            Currency.currency_date == config.date
        ).all()
        for rate in rates:
            export_list.append({
                "currency_code": rate.currency_code,
                "currency_date": rate.currency_date.isoformat(),
                "currency_name": rate.currency_name,
                "currency_scale": rate.currency_scale,
                "currency_rate": float(rate.currency_rate),
                "email": config.email,
            })

    if export_list:
        logger.info(f"Отправка {len(export_list)} записей в WORKER на экспорт")
        app.send_task("worker.tasks.export_rates_to_file_and_email", args=[json.dumps(export_list)])
    else:
        logger.info("Нет данных для экспорта")

    session.close()
    logger.info("Завершена задача: export_data_and_send_to_email")
