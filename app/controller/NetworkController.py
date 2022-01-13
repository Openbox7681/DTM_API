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
            "Data": data,
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
        networkMap = {}
        # get dns list
        dnsBlocks = os.popen('systemd-resolve --status').read().split('\n\n')
        for dnsNetwork in dnsBlocks:
            if not dnsNetwork.startswith('Link'):
                continue
            lines = dnsNetwork.split('\n')
            name = lines[0].split('(')[1].split(')')[0]
            networkMap[name] = {}
            networkMap[name]['DNS'] = []
            for dns in dnsNetwork.split('DNS Servers:')[1].split('\n'):
                networkMap[name]['DNS'].append(dns.strip())

        # get gateway
        gatewayBlocks = os.popen('nmcli dev show').read().split('\n\n')
        for gatewayLines in gatewayBlocks:
            for line in gatewayLines.split('\n'):
                if 'GENERAL.DEVICE' in line:
                    name = line.split(' ')[-1]
                if 'IP4.GATEWAY' in line and name in networkMap:
                    gateway = line.split(' ')[-1]
                    networkMap[name]['Gateway'] = gateway

        # get network info
        networkList = []
        ifconfig = os.popen('ifconfig').read().strip().split('\n\n')
        for networkString in ifconfig:
            network = {}
            lines = networkString.split('\n')
            network['Name'] = lines[0].split(':')[0]
            if network['Name'] == 'lo':
                continue
            secondLines = lines[1].strip().split(' ')
            network['Ip'] = secondLines[1]
            network['Netmask'] = secondLines[4]
            network['Mac'] = lines[3].strip().split(' ')[1]
            network['DNS'] = networkMap[network['Name']]['DNS']
            network['Gateway'] = networkMap[network['Name']]['Gateway']
            networkList.append(network)


        status = 200
        message = 'success'
        data = networkList
        # data = [
        #     {
        #         'Name': 'enp0s8',
        #         'Ip': '192.168.0.202',
        #         'Netmask': '255.255.255.0',
        #         'Mac': '08:00:27:66:ef:5a',
        #         'DNS': [''],
        #         'Gateway': '',
        #         'Trafic': {
        #             'Max': 2000,
        #             'Min': 100,
        #             'Average': 1400,
        #             'List': [
        #                 {'timestamp': 1641318528, 'flow': 200},
        #                 {'timestamp': 1641318528, 'flow': 100},
        #                 {'timestamp': 1641318528, 'flow': 600},
        #                 {'timestamp': 1641318528, 'flow': 800},
        #                 {'timestamp': 1641318528, 'flow': 2000},
        #                 {'timestamp': 1641318528, 'flow': 1800},
        #                 {'timestamp': 1641318528, 'flow': 1600},
        #                 {'timestamp': 1641318528, 'flow': 1600},
        #                 {'timestamp': 1641318528, 'flow': 1600},
        #                 {'timestamp': 1641318528, 'flow': 1600},
        #             ]
        #         }
        #     },
        #     {
        #         'Name': 'enp0s9',
        #         'Ip': '192.168.0.203',
        #         'Netmask': '255.255.255.0',
        #         'Mac': '08:00:27:8b:76:f3',
        #         'Trafic': {
        #             'Max': 2000,
        #             'Min': 100,
        #             'Average': 1400,
        #             'List': [
        #                 {'timestamp': 1641318528, 'flow': 200},
        #                 {'timestamp': 1641318528, 'flow': 100},
        #                 {'timestamp': 1641318528, 'flow': 600},
        #                 {'timestamp': 1641318528, 'flow': 800},
        #                 {'timestamp': 1641318528, 'flow': 2000},
        #                 {'timestamp': 1641318528, 'flow': 1800},
        #                 {'timestamp': 1641318528, 'flow': 1600},
        #                 {'timestamp': 1641318528, 'flow': 1600},
        #                 {'timestamp': 1641318528, 'flow': 1600},
        #                 {'timestamp': 1641318528, 'flow': 1600},
        #             ]
        #         }
        #     }
        # ]
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
        file = os.popen('cat /etc/ntp.conf').read()
        NtpContent = file.split('# more information.')[-1].split('# Use Ubuntu\'s ntp server as a fallback.')[0].strip()
        data = {
            'NtpContent': NtpContent
        }
        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data,
        })

    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('NtpContent', type=str, location='json', required=True) \
            .parse_args()

        NtpContent = args['NtpContent']

        file = os.popen('cat /etc/ntp.conf').read()
        newFile = f"{file.split('# more information.')[0]}# more information.\n{NtpContent}\n# Use Ubuntu{file.split('# Use Ubuntu')[-1]}"

        try:
            with open('/etc/ntp.conf', 'w') as f:
                f.write(newFile)
            
            status = 200
            message = 'success'
            data = os.popen('sudo service ntp restart').read()
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data,
        })
