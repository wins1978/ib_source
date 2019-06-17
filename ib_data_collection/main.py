import datetime
import collections
import inspect
import sys
import threading
import time
from common import *

from ibapi import wrapper
from ibapi import utils
from ibapi.client import EClient
from ibapi.utils import iswrapper

# types
from ibapi.common import * # @UnusedWildImport
from ibapi.order_condition import * # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import * # @UnusedWildImport
from ibapi.order_state import * # @UnusedWildImport
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter
from ibapi.commission_report import CommissionReport
from ibapi.ticktype import * # @UnusedWildImport
from ibapi.tag_value import TagValue
from ibapi.account_summary_tags import *
from ibapi.scanner import ScanData

from test_client import *
from test_wrapper import *
from contract import *
from pika_mq import *

def printinstance(inst:Object):
    attrs = vars(inst)
    print(', '.join("%s: %s" % item for item in attrs.items()))

class TestApp(TestWrapper, TestClient):
    def __init__(self,bizType):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)

        self.bizType = bizType
        self.started = False
        self.nextValidOrderId = None
        
        global contract_idx
        contract_idx = 1
        print("STARTING ..." + self.bizType)    

    @iswrapper
    def connectAck(self):
        if self.asynchronous:
            self.startApi()


    @iswrapper
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)

        self.start()

    def start(self):
        if self.started:
            return
        self.started = True
        self.mq = PikaMQ()
        if self.bizType == "list_contract":
            self.contractOperations()
        elif self.bizType == "by_day":
            self.monitoringHistoricalDataByDay()
        else :
            print("ERROR bizType")

    # =======================================================
    # Refresh Contract
    # =======================================================
    # There must be an interval of at least 1 second between successive calls to reqMatchingSymbols
    def contractOperations(self):
        global contract_idx
        contract_idx = contract_idx +1
        # check lock flag
        # get random names ...
        # loop
        self.callContractMethod(200000 + contract_idx, "IBKR")
        
        timer = threading.Timer(2,self.contractOperations)
        timer.start()
    
    def callContractMethod(self,idx,name):
        self.reqMatchingSymbols(idx, name)

    @iswrapper
    # ! [symbolSamples]
    def symbolSamples(self, reqId: int,
                      contractDescriptions: ListOfContractDescription):
        super().symbolSamples(reqId, contractDescriptions)
        print("Symbol Samples. Request Id: ", reqId)

        for contractDescription in contractDescriptions:
            logging.info("----"+contractDescription.contract.symbol)
            derivSecTypes = ""
            for derivSecType in contractDescription.derivativeSecTypes:
                derivSecTypes += derivSecType
                derivSecTypes += " "
            print("Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, "
                  "currency:%s, derivativeSecTypes:%s" % (
                contractDescription.contract.conId,
                contractDescription.contract.symbol,
                contractDescription.contract.secType,
                contractDescription.contract.primaryExchange,
                contractDescription.contract.currency, derivSecTypes))
    # ! [symbolSamples]
    
    # =======================================================
    # Refresh Historical Data
    # =======================================================
    def monitoringHistoricalDataByDay(self):
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
        print(queryTime)
        self.reqHistoricalData(400000, ContractSamples.StockGOOG(), queryTime,"2 M", "1 day", "MIDPOINT", 1, 1, False, [])

    @iswrapper
    def historicalData(self, reqId:int, bar: BarData):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)
        msg = "ReqType: HistoricalData, ReqId: " +str(reqId) +", " + str(bar)
        self.mq.send(msg)

    @iswrapper
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
        # msg = "ReqType: HistoricalDataEnd, ReqId: " +str(reqId)
        # self.mq.send(msg)

    @iswrapper
    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)

    # =======================================================
    # Main
    # =======================================================
def main():
    SetupLogger()

    businessType = sys.argv[1]
    if businessType == "":
        print("no businessType")
        return

    try:
        app = TestApp(businessType)
        # 127.0.0.1 119.29.185.247
        # TEST 4002, PROD 4001
        app.connect("119.29.185.247", 4001, clientId=0)

        app.run()
    except:
        raise
    finally:
        app.mq.close()
        logging.error("END")

if __name__ == "__main__":
    main()