FROM python:3.10.13-alpine

WORKDIR /app

RUN apk update
RUN apk add --no-cache gcc libc-dev librdkafka-dev musl-dev

COPY ./producer/* /app/.
COPY ./models/ /app/models/
COPY ./services/ /app/services/

RUN pip install -r requirements.txt

CMD python3 kafka_producer.py
