from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required ,get_jwt_identity

import app.model.SystemInfo as system
from datetime import datetime
from app import jwt


class GetSuricataLog(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        status = None
        data = dict()

        args = reqparse.RequestParser() \
            .add_argument("Size", type=int, location='json', required=True) \
            .parse_args()
        
        size = 10 if args["Size"] is None else args["Size"]

        try : 
            status = 200
            message = 'success'
            data = system.get_suricata_log(size)
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class GetDTMLog(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        status = None
        data = dict()

        args = reqparse.RequestParser() \
            .add_argument("Size", type=int, location='json', required=True) \
            .parse_args()
        
        size = 10 if args["Size"] is None else args["Size"]

        try : 
            status = 200
            message = 'success'
            data = system.get_dtm_log(size)
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })