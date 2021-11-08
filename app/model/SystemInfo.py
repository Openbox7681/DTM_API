import psutil
import socket

#取得CPU資訊
def get_CpuInfo():
    response = dict()
    #cpu 數量
    cpuCount = psutil.cpu_count()
    #per cpu count 使用率
    cpuPerList = psutil.cpu_percent(interval=2, percpu=True)
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
