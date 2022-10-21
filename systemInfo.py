import psutil
from psutil._common import bytes2human


def getRAM():
    svmem=psutil.virtual_memory()
    return svmem.percent
    # total=""
    # used=""
    # for name in psutil.virtual_memory()._fields:
    #     value = getattr(psutil.virtual_memory(), name)
    #     if name == 'total':
    #         total=value
    #     elif name == 'used':
    #         used=value
    # return psutil.perceent

def getCPU():
    return psutil.cpu_percent(interval=1)


# while 1:
#     print ("\n")
#     print ( getCPU() )
#     print (getRAM(psutil.virtual_memory()))
