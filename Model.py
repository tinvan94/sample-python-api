from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class Customers(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    update_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    dob = db.Column(db.Date, nullable=False)

    def __init__(self, name, dob):
        self.name = name
        self.dob = dob

class CustomerSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    update_at = fields.DateTime()
    dob = fields.Date()
