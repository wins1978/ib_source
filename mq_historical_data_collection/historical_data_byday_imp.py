import decimal
import datetime
import logging
import ast
from model.historical_data_byday import HistoricalDataByDay
from model.basic_contract_info import BasicContractInfo
import settings

class HistoricalDataByDayImp:
    @staticmethod
    def receiveData(body):
        dist1 = {}
        msg = body.decode()
        arr = msg.split(",")
        for item in arr:
            keyPair = item.split(":")
            key = keyPair[0].strip()
            value = keyPair[1].strip()
            dist1[key] = value
        
        if dist1["ReqType"] == "HistoricalData":
            close_pri = decimal.Decimal(dist1["Close"])
            high_pri = decimal.Decimal(dist1["High"])
            low_pri = decimal.Decimal(dist1["Low"])
            open_pri = decimal.Decimal(dist1["Open"])
            req_id = int(dist1["ReqId"])
            stock_time = dist1["Date"][0:4] + "-" + dist1["Date"][4:6] + "-" + dist1["Date"][6:8]
            stock_time_str = dist1["Date"]
            time = datetime.datetime.now()
            
            print("----------- %s" %req_id)
            try:
                item = BasicContractInfo.get_by_id(req_id)
                if item != None and item.id >0 :
                    print("insert into %s" %item.symbol)
                    HistoricalDataByDay.insert(symbol=item.symbol,
                        stock_time=stock_time,
                        stock_time_str=stock_time_str,
                        req_id=req_id,
                        open_pri=open_pri,
                        high_pri=high_pri,
                        low_pri=low_pri,
                        close_pri=close_pri,
                        import_time = datetime.datetime.now()
                        ).on_conflict("replace").execute()
                else :
                    logging.error("no record found req_id: %d" %req_id)
            except Exception as e:
                logging.error(e)