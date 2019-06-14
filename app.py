from flask import Blueprint
from flask_restful import Api
from resources.customer import CustomerResource
from resources.user import UserRegistration, UserLogin, UserLogout

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
routes = [
    '/customer/<int:customer_id>',
    '/customer',
]
api.add_resource(CustomerResource, *routes)
api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
