import psutil
import socket
import dns.resolver

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
    print(memory)
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
    interfaceInfo = psutil.net_io_counters(pernic=True)
    interfaceKey = interfaceInfo.keys()
    response = list()
    for interfaceName in interfaceKey:
        responseJson = dict()
        print(interfaceInfo[interfaceName])
        interface_bytes = interfaceInfo[interfaceName]
        responseJson = {
            'Interface' : interfaceName,
            'BytesSent' : interface_bytes.bytes_sent,
            'BytesRecv' : interface_bytes.bytes_recv,
            'PacketsSent' : interface_bytes.packets_sent,
            'PacketsRecv' : interface_bytes.packets_recv
        }
        response.append(responseJson)
    return response







