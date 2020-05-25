FROM python:3.7-alpine

ENV FLASK_APP api.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV REDIS_HOST redis

RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev

# Add the dependencies to the container and install the python dependencies
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . .
CMD ["flask", "run"]