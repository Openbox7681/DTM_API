from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required ,get_jwt_identity

import app.model.SystemInfo as system
from datetime import datetime
from app import jwt
import os

class GetCpuInfo(Resource):
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
            data = system.get_CpuInfo()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)


        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class GetDetection(Resource):
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
            data = system.get_detection()
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
            .add_argument('Detection', type=str, location='json', required=True) \
            .parse_args()
        message = None
        status = None
        data = dict()
        detection = args['Detection']
        try:
            lines = os.popen('cat /etc/suricata/suricata.yaml').read().split('\n')
            newLines = []
            doReplace = False
            for line in newLines:
                if doReplace:
                    newLines.append(f'    HOME_NET: {detection}')
                    doReplace = False
                    continue
                if 'address-groups' in line:
                    doReplace = True
            with open('/etc/dtm/build/dtm.config', 'w') as f:
                f.write('\n'.join(newLines))
            status = 200
            message = 'success'
            data = system.get_detection()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class GetMemoryInfo(Resource):
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
            data = system.get_MemoryInfo()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)


        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class GetDiskInfo(Resource):
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
            data = system.get_DiskInfo()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)


        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class GetAllInterface(Resource):
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
            data = system.get_all_interface()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)


        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


class GetAllInterfaceBytes(Resource):
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
            data = system.get_all_interface_bytes()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data
        })


