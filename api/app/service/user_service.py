import os

import sys
sys.path.append("..")

from app import database

from utils.Logger import Logger
from utils.ApiResponse import ApiResponse

from model.User import User
from model.Token import Token

logger = Logger()

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
    def getLastUserID():
        last_user_query = User.query.order_by(User.created_at).first()
        if last_user_query is None:
            return 0
        else:
            return last_user_query.id
