FROM python:3.7-alpine

# python-ldap requirements
RUN apk update && apk add openldap-dev libc-dev gcc g++

# psycopg2 requirements
RUN apk add libpq python3-dev musl-dev postgresql-dev

COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

# Install WSGI server
RUN pip install gunicorn==20.1.0

WORKDIR /app
COPY ./app /app
ARG FLASK_API_VERSION
RUN pip install -e /app

# Run migrations and WSGI server
COPY ./prod.entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
