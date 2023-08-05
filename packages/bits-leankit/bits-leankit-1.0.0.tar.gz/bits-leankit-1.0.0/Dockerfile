FROM python:3.7-alpine

COPY Pipfile* /usr/src/

RUN apk update \
    && apk add bash curl gcc git libffi-dev libssl1.1 libxml2-dev libxslt-dev make musl-dev openssh-client openssl-dev \
    && pip install pipenv==2018.11.26 --upgrade \
    && cd /usr/src \
    && pipenv lock \
    && pipenv sync --dev \
    && rm -rf /tmp/* \
    && rm -rf /var/cache/apk/* \
    && rm -rf /var/tmp/*

WORKDIR /usr/src

CMD ["bash", "-l"]
