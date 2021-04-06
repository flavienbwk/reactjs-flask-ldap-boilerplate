import os
import ldap
import time
import datetime

from flask import request, escape
from functools import wraps

from ..app import logger

from ..service.token_service import TokenService
from ..service.user_service import UserService

from ..utils.ApiResponse import ApiResponse
from ..utils.hash import sha256, hash_id

from ..model.User import User
from ..model.Token import Token


LDAP_SCHEME = os.environ.get("LDAP_SCHEME")
LDAP_HOST = os.environ.get("LDAP_HOST")
LDAP_PORT = os.environ.get("LDAP_PORT")
LDAP_ENDPOINT = "{}://{}:{}".format(LDAP_SCHEME, LDAP_HOST, LDAP_PORT)
LDAP_USERS_DN = os.environ.get("LDAP_USERS_DN")
LDAP_ADMIN_DN = os.environ.get("LDAP_ADMIN_DN")
LDAP_ADMIN_PASSWORD = os.environ.get("LDAP_ADMIN_PASSWORD")

def requires_authentication(f):
    """
    Middleware decorator for checking token presence
    and validity in the headers. Renews the token for
    each query.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = ApiResponse()
        if "X-Api-Auth-Token" in request.headers:
            token_value = escape(request.headers["X-Api-Auth-Token"])
            response = AuthService.checkToken(token_value)
            if response.error is False:
                response = AuthService.renewToken(token_value)
        else:
            response.setMessage("Missing token in header of the query : X-Api-Auth-Token")

        if response.error is True:
            return response.getResponse()
        else:
            return f(*args, **kwargs)
    return wrapper

class AuthService():

    @staticmethod
    def authLDAPUser(username: str, password: str):
        response = ApiResponse()
        user_details = AuthService.checkLDAPCredentials(username, password)
        if user_details is not False:
            username = user_details[0][1]["uid"][0].decode('utf-8')
            user = User.query.filter_by(username=username).first()

            if user is None:
                # If not yet in database, create user account 
                # from users's LDAP details
                sql_datetime = datetime.datetime.utcnow()
                last_id = (UserService.getLastUserID() + 1)
                first_name = user_details[0][1]["givenName"][0].decode('utf-8')\
                    if "givenName" in user_details[0][1] else "" # givenName is optional in LDAP
                UserService.createUser({
                    "ids": sha256(hash_id(last_id) + str(time.time())),
                    "username": username,
                    "first_name": first_name,
                    "last_name": user_details[0][1]["sn"][0].decode('utf-8'),
                    "created_at": sql_datetime,
                    "updated_at": sql_datetime
                })
                user = User.query.filter_by(username=username).first()

            if user is not None:
                response = UserService.updateLDAPUser(user)
                if (response.error is False):
                    response = TokenService.generateUserToken(user.id)
                    response.message = response.message if (response.error) else "Authentication succeeded" 
            else:
                logger.error("Impossible to find the profile of " + username)
                response.setMessage("Impossible to find your profile")

        else:
            response.setMessage("Invalid username or password")
        return response

    @staticmethod
    def checkLDAPCredentials(username: str, password: str):
        return_value = False
        search_filter = "(&(uid={})(objectClass=inetOrgPerson))".format(username)
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            connection = ldap.initialize(LDAP_ENDPOINT)
            connection.protocol_version = ldap.VERSION3
            connection.simple_bind_s(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)
            result = connection.search_s(LDAP_USERS_DN, ldap.SCOPE_SUBTREE, search_filter)
            if len(result):
                user_dn = result[0][0]
                connection.simple_bind_s(user_dn, password)
                return_value = True
            connection.unbind()
        except ldap.LDAPError as e:
            logger.debug("[AuthService.checkLDAPCredentials] Can't perform LDAP authentication for " + username)
            logger.debug(e)
        return result if return_value is not False else False

    @staticmethod
    def checkToken(token_value: str):
        response = ApiResponse()
        token = TokenService.getValidToken(token_value)
        if token is not None:
            expires_at_dt = datetime.datetime.fromtimestamp(token.ut_expires_at)
            response.setSuccess()
            response.setMessage("Valid token until : " + str(expires_at_dt))
            response.setDetails({ "expires_at": token.ut_expires_at })
        else:
            response.setMessage("Invalid or expired token, please login")
        return response

    @staticmethod
    def renewToken(token_value: str):
        response = ApiResponse()
        token = Token.query.filter_by(token=token_value).order_by(Token.ut_created_at.desc()).first()
        if token is None:
            response.setMessage("Token was not found")
            logger.error("Token was not found. Token: " + token_value)
            return response
        user = User.query.filter_by(id=token.User_id).first()
        if user is None:
            response.setMessage("No user was found associated with this token")
            logger.error("No user was found associated with this token. Token.id: {}".format(
                token.id
            ))
            return response
        return TokenService.renewToken(token.id)

    @staticmethod
    def removeToken(token_value: str):
        response = ApiResponse()
        token = Token.query.filter_by(token=token_value).order_by(Token.ut_created_at.desc()).first()
        if token is None:
            response.setMessage("Token was not found")
            logger.error("Token was not found. Token: " + token_value)
            return response
        response = TokenService.removeToken(token.id)
        if response.error is False:
            response.setMessage("You've correctly been logged out.")
        return response
