import json
from typing import Dict, Union

class ApiResponse():
    """
    A class that formats correctly the expected
    response from the web applicaiton.

    @author : github.com/flavienbwk | berwic_f
    """

    def __init__(self) -> None:
        self.error = True
        self.message = ""
        self.details = {}
        self.http_code = 400

    def setAll(self, error: bool, message: str, details: dict, http_code: int = 400) -> None:
        self.error = error
        self.message = message
        self.details = details
        self.http_code = http_code

    def setSuccess(self) -> None:
        self.http_code = 200
        self.error = False

    def setError(self) -> None:
        self.http_code = 400
        self.error = True
    
    def setMessage(self, message: str) -> None:
        self.message = message

    def setDetails(self, details: dict) -> None:
        self.details = details

    def setHTTPCode(self, http_code: int) -> None:
        self.http_code = http_code

    def getResponse(self) -> {"http_code": int, "error": bool, "message": str, "data": {}}:
        return {
            "flask_api": True,
            "http_code": self.http_code,
            "error": self.error,
            "message": self.message,
            "data": self.details
        }

    @staticmethod
    def formatFlaskResponse(response):
        """
        Formatting response to a unique format while
        still benefiting of the Swagger marshaling.

        Switching from the Flask "errors" key to
        response format with "error" & "message".
        
        Adding an empty "data" object if no details
        are returned, to remain consistent.
        """
        try:
            # Checking if response is from our Flask API.
            # Maybe it is from Swagger UI
            response_data = json.loads(response.get_data())
            if "flask_api" not in response_data:
                return response, response._status_code
            else:
                del response_data["flask_api"]
        except ValueError:
            return response, response._status_code

        http_code = 200
        response.headers.add('Content-Type', 'application/json')
        if "errors" in response_data:
            response_data["message"] = ApiResponse.stringifyFlaskErrors(response_data["errors"])
            response_data["error"] = True
            del(response_data["errors"])
        if "data" not in response_data:
            response_data["data"] = {}
        if "error" not in response_data:
            response_data["error"] = True
        if "http_code" in response_data:
            http_code = response_data["http_code"] if response_data["error"] is True else 200
            del response_data["http_code"]
        else:
            http_code = 400 if response_data["error"] is True else 200
        response.set_data(json.dumps(response_data))
        return response, http_code

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
        return "<ApiResponse(error='{}', message='{}', details={}, http_code={})>".format(
            self.error,
            self.message,
            len(self.details),
            self.http_code
        )
