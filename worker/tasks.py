import os
from collections import defaultdict

from worker.celery import app
from worker.logger import setup_logger
import requests
import json
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

logger = setup_logger("worker.tasks")


@app.task
def fetch_rates_from_api(currency_code, date):
    logger.info(f"Получение курса валюты {currency_code} на {date}")
    url = f"https://www.nbrb.by/api/exrates/rates?ondate={date}&periodicity=0"
    response = requests.get(url)
    rates = response.json()

    for rate in rates:
        if rate["Cur_Abbreviation"] == currency_code:
            data = {
                "id": rate["Cur_ID"],
                "currency_date": date,
                "currency_code": rate["Cur_Abbreviation"],
                "currency_scale": rate["Cur_Scale"],
                "currency_name": rate["Cur_Name"],
                "currency_rate": rate["Cur_OfficialRate"]
            }
            logger.info(f"Отправка курса валюты {rate['Cur_Abbreviation']} в CORE")
            app.send_task("core.tasks.save_rates", args=[json.dumps(data)])
            return

    logger.warning(f"Валюта {currency_code} не найдена в ответе API")


@app.task
def export_rates_to_file_and_email(json_data):
    filename = "exported_rates.json"
    logger.info(f"Сохранение данных в файл: {filename}")

    grouped_data = defaultdict(list)
    for entry in json.loads(json_data):
        grouped_data[entry['email']].append(entry)

    result = list(grouped_data.values())

    for idx, group in enumerate(result, 1):

        with open(filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(group))

        smtp_server = os.getenv('EMAIL_SMTP_SERVER')
        smtp_port = os.getenv('EMAIL_SMTP_PORT')
        sender = os.getenv('EMAIL_SMTP_USER')
        receiver = group[0].get('email', None)
        password = os.getenv('EMAIL_SMTP_PASSWORD')

        msg = MIMEMultipart()
        msg["Subject"] = "Экспорт курсов валют"
        msg["From"] = sender
        msg["To"] = receiver
        msg.attach(MIMEText("Во вложении файл с курсами валют."))

        with open(filename, "rb") as file:
            part = MIMEApplication(file.read(), Name=filename)
            part["Content-Disposition"] = f'attachment; filename="{filename}"'
            msg.attach(part)
        try:
            logger.info(f"Отправка письма на {receiver}")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(sender, password)
                server.sendmail(sender, receiver, msg.as_string())
            logger.info("Письмо успешно отправлено")
        except Exception as e:
            logger.error(f"Ошибка при отправке email: {e}")
