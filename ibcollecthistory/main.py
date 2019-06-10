import datetime
import collections
import inspect
from Common import *

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

from TestClient import *
from TestWrapper import *
from ContractSamples import *


class TestApp(TestWrapper, TestClient):
    def __init__(self):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)

        self.started = False
        self.nextValidOrderId = None


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
        self.historicalDataOperations_req()

    def historicalDataOperations_req(self):
        # Requesting historical data
        # ! [reqHeadTimeStamp]
        # self.reqHeadTimeStamp(4101, ContractSamples.USStockAtSmart(), "TRADES", 0, 1)
        # ! [reqHeadTimeStamp]

        # ! [reqhistoricaldata]
        #queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d %H:%M:%S")
        self.reqHistoricalData(4102, ContractSamples.StockGOOG(), queryTime,
                               "1 Y", "1 day", "MIDPOINT", 1, 1, False, [])
        self.reqHistoricalData(4103, ContractSamples.StockTQQQ(), queryTime,
                               "1 Y", "1 day", "MIDPOINT", 1, 1, False, [])
        # self.reqHistoricalData(4103, ContractSamples.EuropeanStock(), queryTime, "10 D", "1 min", "TRADES", 1, 1, False, [])
        #self.reqHistoricalData(4104, ContractSamples.EurGbpFx(), "", "1 M", "1 day", "MIDPOINT", 1, 1, True, [])
        # ! [reqhistoricaldata]

    @iswrapper
    # ! [historicaldata]
    def historicalData(self, reqId:int, bar: BarData):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)
    # ! [historicaldata]

    @iswrapper
    # ! [historicaldataend]
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
    # ! [historicaldataend]

    @iswrapper
    # ! [historicalDataUpdate]
    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)
    # ! [historicalDataUpdate]

def main():
    SetupLogger()
    logging.info("STARTING IB...")

    try:
        app = TestApp()
        # 127.0.0.1 119.29.185.247
        # TEST 4002, PROD 4001
        app.connect("127.0.0.1", 4001, clientId=0)

        app.run()
    except:
        raise
    finally:
        logging.error("END")

if __name__ == "__main__":
    main()