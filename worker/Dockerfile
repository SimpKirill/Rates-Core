FROM python:3.8-slim

WORKDIR /Rates-Core

COPY ./worker/requirements.txt /Rates-Core/worker/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /Rates-Core/worker/requirements.txt

COPY ./worker /Rates-Core/worker

ENV PYTHONPATH="/Rates-Core"

EXPOSE 5672 15672 5432

COPY ./worker/start.sh /Rates-Core/worker/start.sh
RUN chmod +x /Rates-Core/worker/start.sh

CMD ["./worker/start.sh"]