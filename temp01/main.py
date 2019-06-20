import datetime
import collections
import inspect
import sys
import threading
import time
from common import *
import os

import settings
settings.init()

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

from model.basic_contract_random_name_task import BasicContractRandomNameTask
from model.basic_contract_random_name import BasicContractRandomName
from model.basic_contract_info import BasicContractInfo

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
        global cidx
        cidx = 1
        print("STARTING ..." + self.bizType)    

    @iswrapper
    def connectAck(self):
        if self.asynchronous:
            self.startApi()

    @iswrapper
    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        super().error(reqId, errorCode, errorString)
        if reqId == -1 :
            return
        if self.bizType == "by_day":
            print("My--Error. Id:", reqId, "Code:", errorCode, "Msg:", errorString, "bizType", self.bizType)
            errorList = {162: "", 200: ""}
            if errorCode in errorList:
                # 200 Invalid destination exchange specified
                # 162 No data of type EODChart is available for the exchange 'DOLLR4LOT'
                print("error---:%d" %errorCode)
                self.updateBasicContractInvalidFlag(reqId)


    @iswrapper
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)

        self.start()

    def start(self):
        print("-----------")
        if self.started:
            return
        self.started = True
        self.monitoringHistoricalDataByDay()

    # =======================================================
    # Refresh Basic Contract --refresh_contract
    # =======================================================
    # There must be an interval of at least 1 second between successive calls to reqMatchingSymbols
    def refreshBasicContract(self):
        global contract_idx
        contract_idx = contract_idx +1
        # get lock flag
        u0 = BasicContractRandomNameTask.get(BasicContractRandomNameTask.task_name == "SymbolRandom")
        if u0.task_status != "DONE":
            print("exit with :"+u0.task_status)
            timer = threading.Timer(12,self.refreshBasicContract)
            timer.start()
            return

        print("update flag")
        u1 = BasicContractRandomNameTask(task_status="RUNNING",last_update_time=datetime.datetime.now())
        u1.id = u0.id
        u1.save()

        # get random names ...
        nameList = BasicContractRandomName.select().order_by(BasicContractRandomName.last_update_date.asc()).limit(10)
        for row in nameList:
            print("searching "+row.name)
            time.sleep(1)

            self.reqMatchingSymbols(200000 + contract_idx, row.name)
            contract_idx = contract_idx +1

       
        
        # start timer
        timer = threading.Timer(2,self.refreshBasicContract)
        timer.start()

    def updateFlagWithExit(self):
        u0 = BasicContractRandomNameTask \
        .update(task_status="DONE",last_update_time=datetime.datetime.now()) \
        .where(BasicContractRandomNameTask.task_name == "SymbolRandom") \
        .execute()

    @iswrapper
    # ! [symbolSamples]
    def symbolSamples(self, reqId: int,
                      contractDescriptions: ListOfContractDescription):
        super().symbolSamples(reqId, contractDescriptions)
        print("Symbol Samples. Request Id: ", reqId)

        for ct in contractDescriptions:
            derivSecTypes = ""
            for derivSecType in ct.derivativeSecTypes:
                derivSecTypes += derivSecType
                derivSecTypes += " "
            
            if ct.contract.currency != "USD":
                continue

            BasicContractInfo.insert(symbol=ct.contract.symbol,
                sec_type=ct.contract.secType,
                currency=ct.contract.currency,
                primary_exchange=ct.contract.primaryExchange,
                last_byday_import_date=datetime.datetime.now(),
                create_time=datetime.datetime.now()
                ).on_conflict("replace").execute()

            print("Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, "
                  "currency:%s, derivativeSecTypes:%s" % (
                ct.contract.conId,
                ct.contract.symbol,
                ct.contract.secType,
                ct.contract.primaryExchange,
                ct.contract.currency, derivSecTypes))
    # ! [symbolSamples]
    
    # =======================================================
    # Refresh Historical Data --by_day
    # =======================================================
    # The maximum number of simultaneous open historical data requests from the API is 50(30 better)
    # Making identical historical data requests within 15 seconds
    # Making six or more historical data requests for the same Contract, Exchange and Tick Type within two seconds
    # Making more than 60 requests within any ten minute period
    def monitoringHistoricalDataByDay(self):
        print("-------------------monitoringHistoricalDataByDay")
        global cidx
        #items = BasicContractInfo.select().where((BasicContractInfo.symbol == "GOOG") & ((BasicContractInfo.primary_exchange == "NYSE") | (BasicContractInfo.primary_exchange == "NASDAQ.NMS"))).order_by(BasicContractInfo.update_time.asc()).limit(1)
        items = BasicContractInfo.select().where(BasicContractInfo.symbol == "GOOG").order_by(BasicContractInfo.update_time.asc()).limit(1)
        
        print("-----------------%s" %items)
        for row in items:
            print("-----------------%s" %items)
            stock = ContractSamples.StockByName(row.sec_type,row.symbol,row.primary_exchange,row.currency)
            queryTime = None
            queryTimeStr = ""
            day = 2200
            durationString = "1 D"
            queryTime = (datetime.datetime.now() - datetime.timedelta(days=30))
               

            queryTimeStr = queryTime.strftime("%Y%m%d %H:%M:%S")
            self.reqHistoricalData(row.id, stock, queryTimeStr,durationString, "1 day", "MIDPOINT", 1, 1, False, [])
            cidx = cidx +1

    def updateBasicContractInvalidFlag(self,id):
        item = BasicContractInfo.get_by_id(id)
        if item != None and item.id >0 :
            u1 = BasicContractInfo(disabled = "Y")
            u1.id= item.id
            u1.save()

    @iswrapper
    def historicalData(self, reqId:int, bar: BarData):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)
        msg = "ReqType: HistoricalData, ReqId: " +str(reqId) +", " + str(bar)

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

    client_id = 41
   

    try:
        app = TestApp("by_day")
        # 127.0.0.1 119.29.185.247
        # TEST 4002, PROD 4001
        app.connect("119.29.185.247", 4001, clientId=50)

        app.run()
    except:
        raise
    finally:
        logging.error("END")

if __name__ == "__main__":
    main()