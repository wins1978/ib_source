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
        print(msg)
        logging.info(msg)
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
            
            try:
                item = BasicContractInfo.get_by_id(req_id)
                if item != None and item.id >0 :
                    with settings.db.atomic() as transaction:
                        try:
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
                            # update time
                            newTime = datetime.datetime.strptime(stock_time, '%Y-%m-%d')
                            needUpdate = 0
                            if item.publish_time == None :
                                needUpdate = 1
                            else :
                                day = (newTime - item.publish_time).days
                                logging.info("newTime: %s, publishTime: %s" %(newTime, item.publish_time))
                                if day >0 :
                                   needUpdate = 1 
                            if needUpdate == 1 :
                                logging.info("update BasicContractInfo: %s" %newTime)
                                print("update BasicContractInfo: %s" %newTime)
                                u2 = BasicContractInfo(publish_time=newTime)
                                u2.id = item.id
                                u2.save()
                        except Exception as e:
                            logging.error(e)
                            transaction.rollback()
                else :
                    logging.error("no record found req_id: %d" %req_id)
            except Exception as e:
                logging.error(e)