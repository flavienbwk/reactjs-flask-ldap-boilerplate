# Dockerized ReactJS, Flask, LDAP-auth boilerplate

<p align="center">
    <a href="https://travis-ci.org/flavienbwk/reactjs-flask-ldap-boilerplate.svg?branch=master" target="_blank">
        <img src="https://travis-ci.org/flavienbwk/reactjs-flask-ldap-boilerplate.svg?branch=master"/>
    </a>
</p>
<p align="center">ReactJS + Flask + Docker<br/>boilerplate using a token-based LDAP authentication</p>

> :smiley: Suggestions and feedbacks are [highly appreciated](https://github.com/flavienbwk/reactjs-flask-ldap-boilerplate/issues/new)

> :information_source: The [ReactJS part](https://github.com/flavienbwk/reactjs-flask-ldap-boilerplate/tree/fe/initial-architecture) is under development. [See TODOs](#left-todos).

## Features

- Docker architecture
- LDAP authentication
- Token-based API authentication
- Automatic [token renewal](./api/app/service/auth_service.py#L44) with [a Flask middleware](./api/app/service/auth_service.py#L31)
- Swagger documentation
- Flask-Migrate
- Flask-SQLAlchemy (PostgreSQL was chosen)
- [Logging and logs rotation](./api/app/utils/Logger.py#L12)

## API documentation

I chose to use Swagger to document the API. Just run the API following the steps below and browse to [`http://localhost:5000`](http://localhost:5000)

Here you can take a look at the database architecture scheme :

<p align="center">
    <img src="./api/database.png"/>
</p>

> Reminder : there is no `password` field because we use LDAP for authentication.

## Setting up the API

The API is made to run with an LDAP server for managing users. Whether use the provided Docker LDAP server or remove the conf. in [`docker-compose.yml`](./docker-compose.yml) and use your own LDAP server.

This section will explain to you how to run this project and set-up the LDAP server with one user.

### Starting services

First, please change the database/LDAP passwords and keys in `docker-compose.yml`

Then, run :

```bash
docker-compose up ldap phpldapadmin database adminer -d
```

> **adminer** (PostgreSQL management) will be available through `http://localhost:8082`  
> **phpLDAPAdmin** (LDAP management) will be available through `https://localhost:8081`

### Creating the first user in the LDAP

Access phpLDAPAdmin with : `https://localhost:8081`

If you are not familiar with LDAP, [read my LDAP user creation guide](./CREATE_LDAP_USER.md) to add your first user

### Run the API

The database will be automatically set-up thanks to Flask Migrate and any future modification brought to [models](./api/app/model) will be automatically applied to the database when the API is **restarted**.

```bash
docker-compose up api
```

Access the API and its documentation browsing [`http://localhost:5000`](http://localhost:5000)

## Setting up the web application

:clock9: This step may take quite a lot of time due to npm's initial modules download

Just run :

```bash
# Build is quick, **first** launch is long (expect at least 5 min.)
docker-compose up app
```

You can now enjoy the app on [`http://localhost:8080`](http://localhost:8080)

> :information_source: If you want to add a dependency, just stop & re-launch a `docker-compose up app`. You won't have to wait as for first launch.

## Why using LDAP authentication ?

LDAP services are used in a lot of companies and institutions around the world to manage their user accounts and rights in a central place.

With this boilerplate, you will be able to develop corporate-ready services AND avoid yourself the troubles of developing registration / password forgotten / change password / profile update code.

## Left TODOs

API :

- [P2] Synchronize user LDAP profile in API database once logged in
- [P3] Add LDAPS (secure LDAP) support

App :

- [P3] Add loader when logging in

Architecture :

- [P3] Add "Deploy to prod" guide in README
- [P3] Create a `prod.docker-compose.yml` file that :
  - Uses NGINX with SSL
  - Builds & serves the front-end
  - Disables Swagger UI
- [P4] Improve Docker networks security between containers
