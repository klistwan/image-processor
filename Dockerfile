FROM python:3.7-alpine

ENV FLASK_APP api.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV REDIS_HOST redis

COPY requirements.txt .

RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
