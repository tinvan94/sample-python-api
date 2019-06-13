from flask import request
from flask_restful import Resource
from Model import db, Customers, CustomerSchema
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

customers_schema = CustomerSchema(many=True)
customer_schema = CustomerSchema()

class CustomerResource(Resource):
    @jwt_required
    def get(self, customer_id=False):
        if customer_id:
            customer = Customers.query.filter_by(id=customer_id).first()
            if customer:
                customers = [customer]
            else:
                return {'message': 'Customer already exists'}, 400
        else:
            customers = Customers.query.all()
        customers = customers_schema.dump(customers).data
        return {'status': 'success', 'data': customers}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
           return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = customer_schema.load(json_data)
        if errors:
            return errors, 422
        customer = Customers(
            name=json_data['name'],
            dob=json_data['dob'],
            )

        db.session.add(customer)
        db.session.commit()

        result = customer_schema.dump(customer).data

        return { "status": 'success', 'data': result }, 201

    def put(self):
        json_data = request.get_json(force=True)
        customer_id = json_data['id']
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = customer_schema.load(json_data)
        if errors:
            return errors, 422
        customer = Customers.query.filter_by(id=customer_id).first()
        if not customer:
            return {'message': 'Customer does not exist'}, 400
        customer.name = data['name']
        customer.dob = data['dob']
        db.session.commit()

        result = customer_schema.dump(customer).data
        return { "status": 'success', 'data': result }, 201

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        customer_id = json_data['id']
        customer = Customers.query.filter_by(id=customer_id).delete()
        db.session.commit()

        return { "status": 'delete success'}, 201
