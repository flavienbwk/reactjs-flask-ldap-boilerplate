import time
from uuid import uuid4
from random import randint

from flask import request

from ..app import database

from ..utils.ApiResponse import ApiResponse
from ..utils.hash import sha256, hash_id

from ..model.User import User
from ..model.Token import Token


TOKEN_EXPIRATION_TIME = 60 * 60 * 6

class TokenService():

    @staticmethod
    def generateUserToken(user_id: str):
        """
        Creates a token for a specific user.
        Removes any token previously created for the user.
        """
        response = ApiResponse()
        user = User.query.filter_by(id=user_id).first()
        timestamp = time.time()
        timestamp_millis = int(round(timestamp * 1000))
        token_ids = sha256(hash_id(timestamp_millis + randint(0, 9999)))
        token_value = sha256(hash_id(timestamp_millis) + str(uuid4()))
        expires_at = int(timestamp + TOKEN_EXPIRATION_TIME)
        if user:
            token = Token(
                ids=token_ids,
                ip=request.remote_addr,
                token=token_value,
                User_id=user.id,
                ut_created_at=timestamp,
                ut_expires_at=expires_at
            )
            TokenService.clearUserTokens(user.id)
            if database.save_changes(token) is False:
                response.setMessage("An error occured while persisting data to the database")
            else:
                response.setSuccess()
                response.setMessage("Token successfuly generated")
                response.setDetails({
                    "token": token_value,
                    "expires_at": expires_at
                })
        else:
            response.setMessage("User not found in the database")
        return response

    @staticmethod
    def renewToken(token_id: int):
        """
        Renews a token for the maximum expiration time.
        """
        response = ApiResponse()
        timestamp = time.time()
        expires_at = int(timestamp + TOKEN_EXPIRATION_TIME)
        token = Token.query.filter_by(id=token_id).first()
        token.ut_expires_at = expires_at
        if database.save_changes(token) is False:
            response.setMessage("An error occured while renewing the token in the database")
        else:
            response.setSuccess()
            response.setMessage("Token successfuly renewed")
            response.setDetails({
                "token": token.token,
                "expires_at": expires_at
            })
        return response

    @staticmethod
    def removeToken(token_id: int):
        """
        Renews a token for the maximum expiration time.
        """
        response = ApiResponse()
        Token.query.filter_by(id=token_id).delete()
        if database.save_changes() is False:
            response.setMessage("An error occured while removing the token from the database")
        else:
            response.setSuccess()
            response.setMessage("Token successfuly removed")
        return response

    @staticmethod
    def clearUserTokens(user_id: int):
        data = Token.query.filter(Token.User_id == user_id).delete()
        database.save_changes(data)

    @staticmethod
    def getValidToken(token_value: str):
        return Token.query.filter(Token.token == token_value).filter(Token.ut_expires_at >= time.time()).first()


