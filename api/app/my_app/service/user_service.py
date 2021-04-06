import os
import ldap
import json
import datetime
from validate_email import validate_email

from ..app import database, logger

from ..utils.ApiResponse import ApiResponse

from ..model.User import User
from ..model.Token import Token


LDAP_SCHEME = os.environ.get("LDAP_SCHEME")
LDAP_HOST = os.environ.get("LDAP_HOST")
LDAP_PORT = os.environ.get("LDAP_PORT")
LDAP_ENDPOINT = "{}://{}:{}".format(LDAP_SCHEME, LDAP_HOST, LDAP_PORT)
LDAP_USERS_DN = os.environ.get("LDAP_USERS_DN")
LDAP_ADMIN_DN = os.environ.get("LDAP_ADMIN_DN")
LDAP_ADMIN_PASSWORD = os.environ.get("LDAP_ADMIN_PASSWORD")

class UserService():
    
    @staticmethod
    def createUser(user_data):
        """
        Creates a user in the database.
        """
        response = ApiResponse()
        user = User.query.filter_by(username=user_data["username"]).first()
        if not user:
            user = User(
                ids=user_data["ids"],
                username=user_data["username"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                created_at=user_data["created_at"],
                updated_at=user_data["updated_at"]
            )
            if database.save_changes(user) is False:
                response.setMessage("An error occured while persisting data to the database")
        else:
            response.setMessage("User already exist in the database")
        return response

    @staticmethod
    def updateLDAPUser(user: User):
        """
        Based on user's username.

        Checks for any change in user database details
        from its LDAP details. Updates any change in the
        database.
        """
        response = ApiResponse()
        search_filter = "(&(uid={})(objectClass=inetOrgPerson))".format(user.username)
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            connection = ldap.initialize(LDAP_ENDPOINT)
            connection.protocol_version = ldap.VERSION3
            connection.simple_bind_s(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)
            ldap_user = connection.search_s(LDAP_USERS_DN, ldap.SCOPE_SUBTREE, search_filter)
            if len(ldap_user):
                ldap_user_details = {
                    "first_name": ldap_user[0][1]["givenName"][0].decode('utf-8')\
                        if "givenName" in ldap_user[0][1] else "", # givenName is optional in LDAP
                    "last_name": ldap_user[0][1]["sn"][0].decode('utf-8')
                }
                user_details = {
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
                response.setSuccess()
                if ldap_user_details != user_details:
                    user.first_name = ldap_user_details["first_name"]
                    user.last_name = ldap_user_details["last_name"]
                    user.updated_at = datetime.datetime.utcnow()
                    if database.save_changes(user) is False:
                        logger.info("User {} was updated from {} to {}".format(
                            user.username,
                            json.dumps(user_details),
                            json.dumps(ldap_user_details)
                        ))
                        response.setError()
                        response.setMessage("An error occured while persisting data to the database")
        except ldap.LDAPError as e:
            logger.debug("[AuthService.updateLDAPUser] Can't perform LDAP search")
            logger.debug(e)
        return response

    @staticmethod
    def getUserByToken(token_value: str):
        user = User.query.join(Token).filter(Token.User_id == User.id).filter(Token.token == token_value).first()
        return user

    @staticmethod
    def getProfile(user: User):
        response = ApiResponse()
        if user is not None:
            response.setSuccess()
            response.setMessage("Details of {} found".format(user.username))
            response.setDetails({
                "ids": user.ids,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "updated_at": user.updated_at
            })
        else:
            response.setMessage("Impossible to find your profile")
        return response

    @staticmethod
    def updateProfile(user: User, updates: dict):
        response = ApiResponse()
        if user is not None:
            perform_update = False
            old_email = user.email
            if "email" in updates:
                if user.email != updates["email"]:
                    if validate_email(updates["email"]):
                        perform_update = True
                        user.email = updates["email"]
                        user.updated_at = datetime.datetime.utcnow()
                    else:
                        response.setMessage("Invalid e-mail address provided")
            if perform_update:
                if database.save_changes(user) is False:
                    response.setMessage("An error occured while saving user's details")
                else:
                    logger.info("[UserService.updateProfile] {}'s email address changed from '{}' to '{}'".format(
                        user.username,
                        old_email,
                        updates["email"]
                    ))
                    response.setMessage("Email successfuly updated")
                    response.setSuccess()
            if len(response.message) == 0:
                response.setMessage("Nothing was updated")
                response.setSuccess()
        else:
            response.setMessage("Impossible to find your profile")
        return response

    @staticmethod
    def getLastUserID():
        last_user_query = User.query.order_by(User.created_at).first()
        if last_user_query is None:
            return 0
        else:
            return last_user_query.id
