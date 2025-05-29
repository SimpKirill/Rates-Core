FROM python:3.8-slim

WORKDIR /Rates-Core

COPY ./core/requirements.txt /Rates-Core/core/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /Rates-Core/core/requirements.txt

COPY ./core /Rates-Core/core

ENV PYTHONPATH="/Rates-Core"

EXPOSE 5672 15672 5432

COPY ./core/start.sh /Rates-Core/core/start.sh
RUN chmod +x /Rates-Core/core/start.sh

CMD ["./core/start.sh"]