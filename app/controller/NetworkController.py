from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import os

from app import jwt


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'status': 201,
        'message': "token expired"
        # 'msg' : jwt_payload
    })


class RebootService(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    # @jwt_required()
    def post(self):
        try:
            status = 200
            message = 'success'
            data = 'it\' rebooting (fake)'
            # data = os.popen('sudo reboot').read()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)
        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class ShutdownService(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    # @jwt_required()
    def post(self):
        try:
            status = 200
            message = 'success'
            # data = os.popen('sudo shutdown').read()
            data = 'it\' shutting down (fake)'
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)
        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class TimezoneService(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    # @jwt_required()
    def get(self):
        try:
            status = 200
            message = 'success'
            data = os.popen('sudo cat /etc/timezone').read()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)
        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })

    def post(self):
        args = reqparse.RequestParser() \
            .add_argument("Timezone", type=str, location='json', required=True)

        try:
            status = 200
            message = 'success'
            data = os.popen(f'sudo timedatectl set-timezone {args["Timezone"]}').read()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)
        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })

