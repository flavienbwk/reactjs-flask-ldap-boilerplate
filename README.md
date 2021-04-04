# Dockerized ReactJS, Flask, LDAP-auth boilerplate

<p align="center">
    <a href="https://travis-ci.org/flavienbwk/reactjs-flask-ldap-boilerplate.svg?branch=master" target="_blank">
        <img src="https://travis-ci.org/flavienbwk/reactjs-flask-ldap-boilerplate.svg?branch=master"/>
    </a>
    <a href="https://codebeat.co/projects/github-com-flavienbwk-reactjs-flask-ldap-boilerplate-master"><img alt="codebeat badge" src="https://codebeat.co/badges/940a0bd0-5aa5-4f96-b6fc-39b6e1b7e14b" /></a>
</p>
<p align="center">ReactJS + Flask + Docker (+ K8S)<br/>boilerplate using a token-based LDAP authentication</p>

> :smiley: Suggestions and feedbacks are [highly appreciated](https://github.com/flavienbwk/reactjs-flask-ldap-boilerplate/issues/new)

## Features

- Docker architecture
- LDAP authentication
- Token-based API authentication
- Automatic [token renewal](./api/app/service/auth_service.py#L44) with [a Flask middleware](./api/app/service/auth_service.py#L31)
- Swagger documentation
- Flask-Migrate
- Flask-SQLAlchemy (PostgreSQL was chosen)
- [Logging and logs rotation](./api/app/utils/Logger.py#L12)
- [Choose](./app/app/src/App.js#L65) between sidebar and navbar (or use both !)
- Responsive design
- Production and development builds

## API documentation

I chose to use Swagger to document the API. Run the API following the steps below and go to [`http://localhost:5000`](http://localhost:5000).

Here you can take a look at the database architecture scheme :

<p align="center">
    <img src="./api/database.png"/>
</p>

> Reminder : there is no `password` field because we use LDAP for authentication.

## Why using LDAP authentication ?

LDAP services are used in a lot of companies and institutions around the world to manage their user accounts and rights in a central place.

With this boilerplate, you will be able to develop corporate-ready services AND avoid yourself the troubles of developing registration / password forgotten / change password / profile update code.

## Getting started (development)

The API is made to run with an LDAP server for managing users. Whether use the provided Docker LDAP server or remove the conf. in [`docker-compose.yml`](./docker-compose.yml) and use your own LDAP server.

This section will explain to you how to run this project and set-up the LDAP server with one user.

### 1. Starting authentication services

1. Copy the `.env.example` to `.env`

    ```bash
    cp .env.example .env
    ```

    > This is a good practice so your `.env` can't be committed along with your modifications (is in `.gitignore`)

2. Change the database/LDAP passwords and keys in `.env`

    Then run :

    ```bash
    docker-compose up ldap phpldapadmin database adminer -d
    ```

- **adminer** (PostgreSQL management) will be available at `http://localhost:8082`  
- **phpLDAPAdmin** (LDAP management) will be available at `https://localhost:8081`

### 2. Creating the first user in the LDAP

Access phpLDAPAdmin at `https://localhost:8081` and [follow the LDAP user creation guide](./CREATE_LDAP_USER.md) to add your first user

### 3. NGINX reverse-proxy

This boilerplate includes NGINX as a reverse proxy so we can have a unique endpoint for our app and API. Else, we would have to open two endpoints : one for the app, the other for the API.

```bash
docker-compose up --build -d nginx
```

NGINX will auto restart until you have started the app and API below.

### 4. Run the API

The database will be automatically set-up thanks to Flask Migrate and any future modification brought to [models](./api/app/model) will be automatically applied when the API is **restarted**.

You might wait some time before the database get updated after starting the API :

```bash
docker-compose up --build -d api
```

> For development, go to [`http://localhost:5000`](http://localhost:5000) to access the API documentation

### 5. Run the web application

:clock9: NPM's initial install may take quite a lot of time

```bash
# Expect several minutes for first launch (npm install)
docker-compose up --build -d app
```

Enjoy the app on [`http://localhost:8080`](http://localhost:8080)

> :information_source: If you want to add a NPM package, just stop & re-launch `docker-compose up app`.
