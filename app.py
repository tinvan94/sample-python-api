from flask import Blueprint
from flask_restful import Api
from resources.customer import CustomerResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
routes = [
    '/customer/<int:customer_id>',
    '/customer',
]
api.add_resource(CustomerResource, *routes)
