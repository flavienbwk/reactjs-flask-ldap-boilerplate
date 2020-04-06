# ReactJS / Flask / LDAP-auth boilerplate

<p align="center">
    <a href="https://travis-ci.org/flavienbwk/reactjs-flask-ldap-docker-boilerplate.svg?branch=master" target="_blank">
        <img src="https://travis-ci.org/flavienbwk/reactjs-flask-ldap-docker-boilerplate.svg?branch=master"/>
    </a>
</p>
<p align="center">ReactJS + Flask + Docker boilerplate using an LDAP and token-based authentication</p>

API includes :

- Docker architecture
- LDAP authentication
- Token-based API authentication
- Automatic [token renewal](./api/app/service/auth_service.py#L44) with [a Flask middleware](./api/app/service/auth_service.py#L31)
- Swagger documentation
- Flask-Migrate
- Flask-SQLAlchemy (PostgreSQL was chosen)
- [Logging and logs rotation](./api/app/utils/Logger.py#L12)

> :information_source: The ReactJS part is under development

## API documentation

I chose to use Swagger to document the API. Just run the API following the steps below and browse to [`http://localhost:5000`](http://localhost:5000)

## Setting up the API

The API is made to run with an LDAP server for managing users. Whether use the provided Docker LDAP server or remove the conf. in [`docker-compose.yml`](./docker-compose.yml) and use your own LDAP server.

This section will explain to you how to run this project and set-up the LDAP server with one user.

### Starting services

First, please change the database/LDAP passwords and keys in `docker-compose.yml`

Then, run :

```
docker-compose up ldap phpldapadmin database adminer -d
```

> **adminer** (PostgreSQL management) will be available through `http://localhost:8082`  
> **phpLDAPAdmin** (LDAP management) will be available through `https://localhost:8081`

### Creating first user in the LDAP

Access phpLDAPAdmin with : `https://localhost:8081`

If you are not familiar with LDAP, [read my LDAP user creation guide](./CREATE_LDAP_USER.md) to add your first user

### Run the API

The database will be automatically set-up thanks to Flask Migrate and any future modification brought to [models](./api/app/model) will be automatically applied to the database when the API is **restarted**.

```
docker-compose up api
```

Access the API and its documentation browsing [`http://localhost:5000`](http://localhost:5000)

Notheless, the API always follows this response schema :

```
{
    "error": boolean,
    "message": string,
    "details": object
}
```

