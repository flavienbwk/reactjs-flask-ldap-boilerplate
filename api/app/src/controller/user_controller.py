from flask import request, escape
from flask_restplus import Resource, Namespace, fields

from ..service.user_service import UserService
from ..service.auth_service import requires_authentication


api = Namespace('User', description='User-related operations')

user_profile_response_dto = api.model('user_profile_response', {
    'error': fields.Boolean(description="True on error, false on success"),
    'message': fields.String(description="Some error or success message"),
    'details': fields.Nested(
        api.model('user_profile_response_details', {
            'ids': fields.String,
            'username': fields.String,
            'first_name': fields.String,
            'last_name': fields.String,
            'email': fields.String,
            'updated_at': fields.DateTime(description="May be updated if LDAP details or email change")
        }), skip_none=True
    )
})

user_profile_update_dto = api.model('user_profile_update', {
    'email': fields.String(required=True, description='New user email')
})

user_profile_update_response_dto = api.model('user_profile_update_response', {
    'error': fields.Boolean(description="True on error, false on success"),
    'message': fields.String(description="Some error or success message"),
    'details': fields.Nested(api.model('user_profile_update_response_details', {}))
})

user_header_token_dto = api.parser()
user_header_token_dto.add_argument(
    'X-Api-Auth-Token', 
    help="Token is renewed each time this header exist", 
    required=True, 
    location='headers'
)

@api.route(
    '/profile', 
    doc={"description": "Performs profile-related actions such has getting et updating details about the user (name, email, username...)"}
)
class Profile(Resource):

    @api.marshal_with(user_profile_response_dto, skip_none=True)
    @api.expect(user_header_token_dto, validate=True)
    @requires_authentication
    def post(self):
        token_value = escape(request.headers["X-Api-Auth-Token"])
        user = UserService.getUserByToken(token_value)
        return UserService.getProfile(user).getResponse()

    @api.marshal_with(user_profile_update_response_dto, skip_none=True)
    @api.expect(user_profile_update_dto, user_header_token_dto, validate=True)
    @requires_authentication
    def put(self):
        token_value = escape(request.headers["X-Api-Auth-Token"])
        user = UserService.getUserByToken(token_value)
        return UserService.updateProfile(user, {
            "email": escape(request.json["email"])
        }).getResponse()
