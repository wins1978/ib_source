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
        self.monitorMarketData()


    def monitorMarketData(self):
        self.reqMarketDataType(MarketDataTypeEnum.DELAYED_FROZEN)
        
        # Requesting real time market data
        self.reqMktData(1000, ContractSamples.StockXNET(), "", False, False, [])
        self.reqMktData(1001, ContractSamples.StockWB(), "", False, False, [])
        self.reqMktData(1002, ContractSamples.StockTQQQ(), "", False, False, [])
        self.reqMktData(1003, ContractSamples.StockMSFT(), "", False, False, [])


    @iswrapper
    # ! [tickprice]
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if price < 0.1:
            return

        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            print("PreOpen:", attrib.preOpen)
        else:
            print()
            print("TickPrice. TickerId:", reqId, "tickType:", tickType,"Price:", price, end=' ')
            #### TODO
    # ! [tickprice]


def main():
    SetupLogger()
    logging.info("STARTING IB...")

    try:
        app = TestApp()
        # 127.0.0.1 119.29.185.247
        # TEST 4002, PROD 4001
        app.connect("127.0.0.1", 4002, clientId=0)

        app.run()
    except:
        raise
    finally:
        logging.error("END")

if __name__ == "__main__":
    main()