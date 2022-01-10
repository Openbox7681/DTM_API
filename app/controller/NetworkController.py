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
            # data = os.popen('sudo reboot').read().strip()
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
            # data = os.popen('sudo shutdown').read().strip()
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
            data = os.popen('sudo cat /etc/timezone').read().strip()
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
            .add_argument("Timezone", type=str, location='json', required=True) \
            .parse_args()
        try:
            status = 200
            message = 'success'
            data = os.popen(f'sudo timedatectl set-timezone {args["Timezone"]}').read().strip()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)
        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class NetworkService(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self):
        status = 200
        message = 'success'
        data = [
            {
                'Name': 'enp0s8',
                'Ip': '192.168.0.202',
                'Netmask': '255.255.255.0',
                'Mac': '08:00:27:66:ef:5a',
                'Trafic': {
                    'Max': 2000,
                    'Min': 100,
                    'Average': 1400,
                    'List': [
                        {'timestamp': 1641318528, 'flow': 200},
                        {'timestamp': 1641318528, 'flow': 100},
                        {'timestamp': 1641318528, 'flow': 600},
                        {'timestamp': 1641318528, 'flow': 800},
                        {'timestamp': 1641318528, 'flow': 2000},
                        {'timestamp': 1641318528, 'flow': 1800},
                        {'timestamp': 1641318528, 'flow': 1600},
                        {'timestamp': 1641318528, 'flow': 1600},
                        {'timestamp': 1641318528, 'flow': 1600},
                        {'timestamp': 1641318528, 'flow': 1600},
                    ]
                }
            },
            {
                'Name': 'enp0s9',
                'Ip': '192.168.0.203',
                'Netmask': '255.255.255.0',
                'Mac': '08:00:27:8b:76:f3',
                'Trafic': {
                    'Max': 2000,
                    'Min': 100,
                    'Average': 1400,
                    'List': [
                        {'timestamp': 1641318528, 'flow': 200},
                        {'timestamp': 1641318528, 'flow': 100},
                        {'timestamp': 1641318528, 'flow': 600},
                        {'timestamp': 1641318528, 'flow': 800},
                        {'timestamp': 1641318528, 'flow': 2000},
                        {'timestamp': 1641318528, 'flow': 1800},
                        {'timestamp': 1641318528, 'flow': 1600},
                        {'timestamp': 1641318528, 'flow': 1600},
                        {'timestamp': 1641318528, 'flow': 1600},
                        {'timestamp': 1641318528, 'flow': 1600},
                    ]
                }
            }
        ]
        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data,
        })


class NTPService(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self):
        status = 200
        message = 'success'
        data = {
            'NtpList': [
                'pool 0.ubuntu.pool.ntp.org iburst',
                'pool 1.ubuntu.pool.ntp.org iburst',
                'pool 2.ubuntu.pool.ntp.org iburst',
                'pool 3.ubuntu.pool.ntp.org iburst',
            ]
        }
        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data,
        })
