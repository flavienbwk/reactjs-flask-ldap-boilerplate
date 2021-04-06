FROM python:3.7-alpine

# python-ldap requirements
RUN apk update && apk add openldap-dev libc-dev gcc g++

# psycopg2 requirements
RUN apk add libpq python3-dev py3-pip musl-dev postgresql-dev

COPY ./app/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]