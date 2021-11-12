import psutil
import socket
import dns.resolver
import time
import os 
import json

#取得Inbound 資訊
def get_bound_info():
    response = dict()
    inbound =os.popen('cat /etc/dtm/build/dtm.config |grep INBOUND').read()
    outbound =os.popen('cat /etc/dtm/build/dtm.config |grep OUTBOUND').read()
    response = {
        "Inbound" : inbound,
        "Outbound" : outbound
    }
    return response

def runService(serviceName):
    response = dict()
    try:
        cmd = 'sudo systemctl start ' + serviceName
        sshServiceStatus = os.popen(cmd)
        return True
    except Exception as e:
        print(e)
        return False

def enableService(serviceName):
    response = dict()
    try:
        cmd = 'sudo systemctl enable ' + serviceName
        sshServiceStatus = os.popen(cmd)
        return True
    except Exception as e:
        print(e)
        return False

def disableService(serviceName):
    response = dict()
    try:
        cmd = 'sudo systemctl disable ' + serviceName
        sshServiceStatus = os.popen(cmd)
        return True
    except Exception as e:
        print(e)
        return False

def stopService(serviceName):
    response = dict()
    try:
        cmd = 'sudo systemctl stop ' + serviceName
        sshServiceStatus = os.popen(cmd)
        return True
    except Exception as e:
        print(e)
        return False

def getAllServiceStatus():

    response = dict()

    sshServiceStatus = os.popen('sudo systemctl status ssh.service |grep Active').read()
    sshServiceIsAuto = os.popen('sudo systemctl is-enabled ssh.service').read()
    tdAgentServiceStatus = os.popen('sudo systemctl status td-agent.service |grep Active').read()
    tdAgentServiceIsAuto = os.popen('sudo systemctl is-enabled td-agent.service').read()
    suricateServiceStatus = os.popen('sudo systemctl status suricata.service |grep Active').read()
    suricateServiceIsAuto = os.popen('sudo systemctl is-enabled suricata.service').read()
    ntpServiceStatus = os.popen('sudo systemctl status ntp.service |grep Active').read()
    ntpServiceIsAuto = os.popen('sudo systemctl is-enabled ntp.service').read()
    dtmServiceStatus = os.popen('sudo systemctl status low-latency-packet-filtering.service |grep Active').read()
    dtmServiceIsAuto = os.popen('sudo systemctl is-enabled low-latency-packet-filtering.service').read()


    response = {
        "SshSeriveIsActive" : 'running' in sshServiceStatus,
        "SshServiceIsAuto" : 'enabled' in sshServiceIsAuto,
        "TdAgentServiceIsActive" : 'running' in tdAgentServiceStatus,
        "TdAgentServiceIsAuto" : 'enabled' in tdAgentServiceIsAuto,
        "SuricateServiceIsActive" : 'running' in suricateServiceStatus,
        "SuricateServiceIsAuto" : 'enabled' in suricateServiceIsAuto,
        "NtpServiceIsActive" : 'running' in ntpServiceStatus,
        "NtpServiceIsAuto" : 'enabled' in ntpServiceIsAuto,
        "DtmServiceIsActive" : 'running' in dtmServiceStatus,
        "DtmServiceIsAuto" : 'enabled' in dtmServiceIsAuto,
    }

    return response


#取得CPU資訊
def get_CpuInfo():
    response = dict()
    #cpu 數量
    cpuCount = psutil.cpu_count()
    #per cpu count 使用率
    cpuPerList = psutil.cpu_percent(interval=1, percpu=True)
    #當前cpu 主頻率
    cpuFreq = psutil.cpu_freq()
    currentCpuFreq = cpuFreq.current
    minCpuFreq = cpuFreq.min
    maxCpuFreq = cpuFreq.max
    hostName = socket.gethostname()
    response = {
        "CpuCount" : cpuCount,
        "CpuPerList" : cpuPerList,
        "CurrentCpuFreq" : currentCpuFreq,
        "MinCpuFreq" : minCpuFreq,
        "MaxCpuFreq" : maxCpuFreq,
        "HostName" : hostName
    }

    return response

#取得Memory資訊
def get_MemoryInfo():
    #Memory資訊
    memory = psutil.virtual_memory()
    response = dict()
    total = memory.total
    available = memory.available
    percent = memory.percent
    used = memory.used
    free = memory.free

    response = {
        "Total" : memory.total,
        "Available" : memory.available,
        "Percent" : memory.percent,
        "Used" : memory.used,
        "Free" : memory.free
    }
    return response

#取得Disk資訊
def get_DiskInfo():
    disk = psutil.virtual_memory()
    response = dict()
    disk = psutil.disk_usage('/') 

    response = {
        "Total" : disk.total,
        "Percent" : disk.percent,
        "Used" : disk.used,
        "Free" : disk.free
    }
    return response

def get_all_interface():
    netInfo = psutil.net_if_addrs()
    interfaceKey =  netInfo.keys()
    response = list()
    dnsIp = dns.resolver.Resolver().nameservers[0]
    for interfaceName in interfaceKey:
        responseJson = dict()
        interface = netInfo[interfaceName][0]
        responseJson = {
            'Interface' : interfaceName,
            'Address' : interface.address,
            'NetMask' : interface.netmask,
            'Broadcast' : interface.broadcast,
            'Dns' : dnsIp
        }
        response.append(responseJson)
    return response

def get_all_interface_bytes():
    interfaceKey,networkIn, networkOut, p_networkIn, p_networkOut = getNetworkRate(2)
    response = list()
    for interfaceName in interfaceKey:
        responseJson = dict()
        responseJson = {
            'Interface' : interfaceName,
            'BytesSent' : networkIn.get(interfaceName) ,
            'BytesRecv' : networkOut.get(interfaceName),
            'PacketsSent' : p_networkIn.get(interfaceName),
            'PacketsRecv' : p_networkOut.get(interfaceName)
        }
        response.append(responseJson)
    return response

#針對特定網卡搜尋資料
def get_interface_bytes(interface):
    interfaceKey,networkIn, networkOut, p_networkIn, p_networkOut = getNetworkRate(2)
    responseJson = dict()
    for interfaceName in interfaceKey:
        if interfaceName == interface:
            responseJson = {
            'Interface' : interfaceName,
            'BytesSent' : networkIn.get(interfaceName) ,
            'BytesRecv' : networkOut.get(interfaceName),
            'PacketsSent' : p_networkIn.get(interfaceName),
            'PacketsRecv' : p_networkOut.get(interfaceName)
        }
    return responseJson

#取得所有網卡
def get_all_interfacesName():
    interfacesName, _, _ , _ ,_ = getNetworkData()
    return interfacesName


def getNetworkData():
    # 取得網卡流量bytes 與封包
    recv = {}
    p_recv = {}
    sent = {}
    p_sent = {}
    data = psutil.net_io_counters(pernic=True)
    interfaces = data.keys()
    for interface in interfaces:
        recv.setdefault(interface, data.get(interface).bytes_recv)
        p_recv.setdefault(interface, data.get(interface).packets_recv)
        sent.setdefault(interface, data.get(interface).bytes_sent)
        p_sent.setdefault(interface, data.get(interface).packets_sent)
    return interfaces, recv, sent, p_recv, p_sent



def getNetworkRate(num):
    # 計算流量速率
    interfaces, oldRecv, oldSent , p_oldRecv, p_oldSent = getNetworkData()
    time.sleep(num)
    interfaces, newRecv, newSent, p_newRecv, p_newSent = getNetworkData()
    networkIn = {}
    p_networkIn = {}
    networkOut = {}
    p_networkOut = {}
    for interface in interfaces:
        networkIn.setdefault(interface, float("%.3f" % ((newRecv.get(interface) - oldRecv.get(interface)) / num)))
        p_networkIn.setdefault(interface, float("%.3f" % ((p_newRecv.get(interface) - p_oldRecv.get(interface)) / num)))
        networkOut.setdefault(interface, float("%.3f" % ((newSent.get(interface) - oldSent.get(interface)) / num)))
        p_networkOut.setdefault(interface, float("%.3f" % ((p_newSent.get(interface) - p_oldSent.get(interface)) / num)))

    return interfaces, networkIn, networkOut, p_networkIn, p_networkOut


def get_suricata_log(size):
    cmd = 'tail -' +  str(size) + ' /var/log/suricata/fast.log'
    loglines = os.popen(cmd).readlines()
    response = list()
    for log in loglines:
        res = dict()
        res = {
            "data" : log
        }
        response.append(res)
    return response


def get_dtm_log(size):
    cmd = 'tail -' +  str(size) + ' /var/log/dtm/daemon.log |grep block |awk -F ] \'{print $3}\' '
    loglines = os.popen(cmd).readlines()
    response = list()
    for log in loglines:
        res = dict()

        data = json.loads(log)
        blockInfo = data['blockinfo']
        blockInfo = [int(item,16) for item in blockInfo.split(" ")]
        SoureIp = '.'.join(map(str, blockInfo[:4]))
        DstIp = '.'.join(map(str, blockInfo[4:8]))
        Port = ''.join(map(str, blockInfo[8:10]))
        Protocol = blockInfo[10]

        res = {
            "SourceIp" : SoureIp,
            "DestinationIp" : DstIp,
            "DestinationPort" : Port,
            "Protocol" : Protocol,
            "Techniques" : "None" if data["signature"] is None else data["signature"] , 
            "Status" : data["status"]
        }
        response.append(res)
    return response