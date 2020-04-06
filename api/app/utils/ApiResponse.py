from typing import Dict, Union

class ApiResponse():
    """
    A class that formats correctly the expected
    response from the web applicaiton.
    """

    def __init__(self) -> None:
        self.errors = True
        self.message = ""
        self.details = {}

    def setAll(self, error: bool, message: str, details: dict) -> None:
        self.errors = error
        self.message = message
        self.details = details

    def setSuccess(self) -> None:
        self.errors = False

    def setError(self) -> None:
        self.errors = True
    
    def setMessage(self, message: str) -> None:
        self.message = message

    def setDetails(self, details: dict) -> None:
        self.details = details

    def getResponse(self) -> {"errors": bool, "message": str, "details": {}}:
        return {
            "errors": self.errors,
            "message": self.message,
            "details": self.details
        }

    def __repr__(self):
        return "<ApiResponse(errors='{}', message='{}', details={})>".format(
            self.errors,
            self.message,
            len(self.details)
        )
