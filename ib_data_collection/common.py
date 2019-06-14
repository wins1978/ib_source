import logging
import time
import os.path

def SetupLogger():
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/ib.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=logging.INFO,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    logger.addHandler(console)

def GetSymbolName():
    name = []
    # 1
    for i in range(ord("A"),ord("Z")+1):
        name.append(chr(i))
    # 2
    for i in range(ord("A"),ord("Z")+1):
        for j in range(ord("A"),ord("Z")+1):
            name.append(chr(i)+chr(j))
    # 3
    # for i in range(ord("A"),ord("Z")+1):
    #     for j in range(ord("A"),ord("Z")+1):
    #         for k in range(ord("A"),ord("Z")+1):
    #             name.append(chr(i)+chr(j)+chr(k))
    # 4
    # for i in range(ord("A"),ord("Z")+1):
    #     for j in range(ord("A"),ord("Z")+1):
    #         for k in range(ord("A"),ord("Z")+1):
    #             for l in range(ord("A"),ord("Z")+1):
    #                 name.append(chr(i)+chr(j)+chr(k)+chr(l))
    return name