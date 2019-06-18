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
        if self.bizType == "refresh_contract":
            self.updateFlagWithExit()
            self.refreshBasicContract()
        elif self.bizType == "by_day":
            self.mq = PikaMQ()
            self.monitoringHistoricalDataByDay()
        else :
            print("ERROR bizType")

    # =======================================================
    # Refresh Contract
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

            # update date
            bcr1 = BasicContractRandomName(last_update_date=datetime.datetime.now())
            bcr1.id=row.id
            bcr1.save()

            self.reqMatchingSymbols(200000 + contract_idx, row.name)
            contract_idx = contract_idx +1

        print("release flag")
        u2 = BasicContractRandomNameTask(task_status="DONE",last_update_time=datetime.datetime.now())
        u2.id = u0.id
        u2.save()    
        
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
        app.connect("127.0.0.1", 4001, clientId=0)

        app.run()
    except:
        raise
    finally:
        if businessType == "by_day":
            app.mq.close()
        logging.error("END")

if __name__ == "__main__":
    main()