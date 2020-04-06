import json
from typing import Dict, Union

class ApiResponse():
    """
    A class that formats correctly the expected
    response from the web applicaiton.
    """

    def __init__(self) -> None:
        self.error = True
        self.message = ""
        self.details = {}

    def setAll(self, error: bool, message: str, details: dict) -> None:
        self.error = error
        self.message = message
        self.details = details

    def setSuccess(self) -> None:
        self.error = False

    def setError(self) -> None:
        self.error = True
    
    def setMessage(self, message: str) -> None:
        self.message = message

    def setDetails(self, details: dict) -> None:
        self.details = details

    def getResponse(self) -> {"error": bool, "message": str, "details": {}}:
        return {
            "error": self.error,
            "message": self.message,
            "details": self.details
        }

    @staticmethod
    def formatFlaskResponse(response):
        """
        Formatting response to a unique format while
        still benefiting of the Swagger marshaling.

        Mainly switching from Flask's "errors" key to
        this repo response format "error" & "message".
        
        Adding an empty "details" object if no details
        are returned to remain consistent.
        """
        response_data = json.loads(response.get_data())
        if "errors" in response_data:
            response_data["message"] = ApiResponse.stringifyFlaskErrors(response_data["errors"])
            response_data["error"] = True
            del(response_data["errors"])
        if "details" not in response_data:
            response_data["details"] = {}
        response.set_data(json.dumps(response_data))
        return response

    @staticmethod
    def stringifyFlaskErrors(obj: object) -> str:
        """
        Turns the list of errors into a string.
        """
        final_message = ""
        for i, message in enumerate(obj.values()):
            final_message += message if i == 0 else ". " + message
        return final_message

    def __repr__(self) -> str:
        return "<ApiResponse(error='{}', message='{}', details={})>".format(
            self.error,
            self.message,
            len(self.details)
        )
