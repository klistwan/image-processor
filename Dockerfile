FROM python:3.7-alpine

ENV FLASK_APP api.py
ENV FLASK_ENV development
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_PORT 5000
ENV REDIS_HOST redis

COPY requirements.txt .

RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev && \
    pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run"]
