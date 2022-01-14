from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import os
import json

from app import jwt
from datetime import timedelta, datetime


binaryMap = {
    '255': 8,
    '254': 7,
    '252': 6,
    '248': 5,
    '240': 4,
    '224': 3,
    '192': 2,
    '128': 1,
    '0': 0,
}

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'status': 201,
        'message': "token expired"
        # 'msg' : jwt_payload
    })


def maskToInt(mask):
    try:
        count = 0
        for binary in mask.split('.'):
            count += binaryMap[binary]
    except:
        raise Exception(f'wrong mask number: {binary}')
    return count


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
        try:
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
                        if name in networkMap:
                            networkMap[name]['Gateway'] = gateway

            # get traffic
            vnstat = json.loads(os.popen('vnstat --json').read())
            interfaces = vnstat['interfaces']
            for interface in interfaces:
                name = interface['id']
                date = interface['updated']['date']
                time = interface['updated']['time']
                startTime = datetime(year=date['year'], month=date['month'], day=date['day'], hour=time['hour']) \
                            + timedelta(days=-1)
                if name in networkMap:
                    networkMap[name]['Traffic'] = {}
                    networkMap[name]['Traffic']['FlowList'] = []
                    hourOffset, minFlow, maxFlow = 0, 9999999, -1
                    sum = 0
                    for hour in interface['traffic']['hours']:
                        traffic = {'rx': hour['rx'], 'tx': hour['tx'], 'time': startTime+timedelta(hours=hourOffset)}
                        if minFlow > traffic['rx']:
                            minDate = traffic['time']
                            minFlow = traffic['rx']
                        if maxFlow < traffic['rx']:
                            maxDate = traffic['time']
                            maxFlow = traffic['rx']
                        networkMap[name]['Traffic']['FlowList'].append(traffic)
                        sum += traffic['rx']
                        hourOffset += 1
                    networkMap[name]['Traffic']['MinFlow'] =  {'MinRx': minFlow, 'MinDate': minDate}
                    networkMap[name]['Traffic']['MaxFlow'] = {'MaxRx': maxFlow, 'MaxDate': maxDate}
                    networkMap[name]['Traffic']['AvgRx'] = sum/24

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
                network['Traffic'] = networkMap[network['Name']]['Traffic']
                networkList.append(network)

            status = 200
            message = 'success'
            data = networkList
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)
        return jsonify({
            "Status": status,
            "Message": message,
            "Data": data,
        })

    def post(self):
        try:
            args = reqparse.RequestParser() \
                .add_argument('Interface', type=str, location='json', required=True) \
                .add_argument('Ip', type=str, location='json', required=True) \
                .add_argument('Netmask', type=str, location='json', required=True) \
                .add_argument('DNS', type=str, location='json', required=True) \
                .parse_args()
            name = args['Interface']
            ip = args['Ip']
            mask = args['Netmask']
            dns = args['DNS']

            newLines = []
            netplanLines = os.popen('cat /etc/netplan/*.yaml').read().split('\n')
            findNextInterface = False
            for line in netplanLines:
                if findNextInterface and 'version' not in line:
                    if line.startswith('    ') and (not line.startswith('      ')):
                        findNextInterface = False
                    else:
                        continue
                if name in line:
                    findNextInterface = True
                    newLines.append(f'    {name}:')
                    newLines.append(f'      addresses: [{ip}/{maskToInt(mask)}]')
                    newLines.append( '      nameservers:')
                    newLines.append(f'        addresses: [{dns}]')
                    newLines.append(f'      dhcp4: false')
                else:
                    newLines.append(line)

            newFile = '\n'.join(newLines)
            with open('/etc/netplan/*.yaml', 'w') as f:
                f.write(newFile)

            os.popen('sudo netplan apply')

            status = 200
            message = 'success'
            data = 'set network ok'
        except Exception as e:
            status = 201
            message = 'error'
            data = str(e)

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
