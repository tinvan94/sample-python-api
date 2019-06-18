from flask import request
from flask_restful import Resource
from Model import db, Users, UserSchema, RevokedToken, RevokedTokenSchema
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserRegistration(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
           return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = Users.query.filter_by(user_name=data['user_name']).first()
        if user:
            return {'message': 'User {} does exist'.format(data['user_name'])}, 400

        #try:
        user = Users(
            user_name=json_data['user_name'],
            password=Users.generate_hash(json_data['password']),
            )
        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data
        access_token = create_access_token(identity=data['user_name'])
        refresh_token = create_refresh_token(identity=data['user_name'])

        return {
            "status": 'success',
            'message': 'User {} was created'.format(result['user_name']),
            'access_token': access_token,
            'refresh_token': refresh_token
                }, 201
        #except:
        #    return {'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
           return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = Users.query.filter_by(user_name=data['user_name']).first()
        if not user:
            return {
                'message': 'User {} doesn\'t  exist'.format(data['user_name']),
                }, 400

        if Users.verify_hash(data['password'], user.password):
            access_token = create_access_token(identity=data['user_name'])
            refresh_token = create_refresh_token(identity=data['user_name'])
            return {
            'message': 'Logged in as {}'.format(user.user_name),
            'access_token': access_token,
            'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}, 400

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
