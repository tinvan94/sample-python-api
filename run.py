from flask import Flask
from Model import RevokedToken

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from Model import db
    db.init_app(app)
    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        query = RevokedToken.query.filter_by(jti=jti).first()
        return query

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)
