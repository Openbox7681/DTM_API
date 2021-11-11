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

class StartService(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        status = None
        data = dict()

        args = reqparse.RequestParser() \
            .add_argument("ServiceName", type=str, location='json', required=True) \
            .parse_args()
        
        ServiceName = None if args["ServiceName"] is None else args["ServiceName"]

        try : 
            status = 200
            message = 'success'
            data = system.runService(ServiceName)
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })

class EnableService(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        status = None
        data = dict()

        args = reqparse.RequestParser() \
            .add_argument("ServiceName", type=str, location='json', required=True) \
            .parse_args()
        
        ServiceName = None if args["ServiceName"] is None else args["ServiceName"]

        try : 
            status = 200
            message = 'success'
            data = system.enableService(ServiceName)
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class StopService(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        status = None
        data = dict()

        args = reqparse.RequestParser() \
            .add_argument("ServiceName", type=str, location='json', required=True) \
            .parse_args()
        
        ServiceName = None if args["ServiceName"] is None else args["ServiceName"]

        try : 
            status = 200
            message = 'success'
            data = system.stopService(ServiceName)
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class DisableService(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        status = None
        data = dict()

        args = reqparse.RequestParser() \
            .add_argument("ServiceName", type=str, location='json', required=True) \
            .parse_args()
        
        ServiceName = None if args["ServiceName"] is None else args["ServiceName"]

        try : 
            status = 200
            message = 'success'
            data = system.disableService(ServiceName)
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })