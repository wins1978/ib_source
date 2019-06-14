from ibapi.contract import * # @UnusedWildImport

class ContractSamples:
    @staticmethod
    def StockTQQQ():
        contract = Contract()
        contract.symbol = "TQQQ"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        #contract.primaryExchange = "ISLAND"
        return contract

    @staticmethod
    def StockMSFT():
        contract = Contract()
        contract.symbol = "MSFT"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        #Specify the Primary Exchange attribute to avoid contract ambiguity 
        #(there is an ambiguity because there is also a MSFT contract with primary exchange = "AEB")
        contract.primaryExchange = "ISLAND"
        return contract

    @staticmethod
    def StockWB():
        contract = Contract()
        contract.symbol = "WB"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        #contract.primaryExchange = "ISLAND"
        return contract

    @staticmethod
    def StockXNET():
        contract = Contract()
        contract.symbol = "XNET"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        #contract.primaryExchange = "ISLAND"
        return contract
    
    @staticmethod
    def StockGOOG():
        contract = Contract()
        contract.symbol = "GOOG"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract