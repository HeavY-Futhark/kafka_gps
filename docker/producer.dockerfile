FROM python:3.10

WORKDIR /app

RUN apt update
RUN apt install -y gcc libc-dev librdkafka-dev musl-dev

COPY ./producer/* /app/.
COPY ./models/ /app/models/
COPY ./services/ /app/services/
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

RUN pip install -r requirements.txt

CMD ["/app/wait-for-it.sh", "kafka:9093", "--", "python3", "kafka_producer.py"]
