from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required ,get_jwt_identity

import app.model.SystemInfo as system
from datetime import datetime
from app import jwt

class GetServiceStatus(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def get(self):
        message = None
        status = None
        data = dict()
        try : 
            status = 200
            message = 'success'
            data = system.getAllServiceStatus()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })