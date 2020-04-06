import os

import sys
sys.path.append("..")

from app import database

from utils.Logger import Logger
from utils.ApiResponse import ApiResponse

from model.User import User

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
    def getLastUserID():
        last_user_query = User.query.order_by(User.created_at).first()
        if last_user_query is None:
            return 0
        else:
            return last_user_query.id
