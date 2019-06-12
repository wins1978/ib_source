import decimal
import ast
from model.historical_data_byday import HistoricalDataByDay
import settings

class HistoricalDataByDayImp:
    @staticmethod
    def receiveData(body):
        print("-----------------------")
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
            symbol = "GOOG"
            
            stock_time = dist1["Date"][0:4] + "-" + dist1["Date"][4:6] + "-" + dist1["Date"][6:8]
            sql = "INSERT INTO historical_data_byday( \
                symbol, req_id, stock_time, stock_time_str, open_pri, high_pri, low_pri, close_pri) \
                VALUES ('%s', %s,  '%s',  '%s',  %s,  %s,  %s,  %s)" % \
                (symbol, req_id, stock_time, stock_time_str, open_pri, high_pri, low_pri, close_pri)
            # insert
            HistoricalDataByDayImp.saveData(sql)
            
    
    @staticmethod    
    def saveData(sql):
        print("insert row..." + sql)
        cursor = settings.db.cursor()
        try:
            cursor.execute(sql)
            settings.db.commit()
        except Exception as e:
            print(e)
            settings.db.rollback()
        #finally:
            #settings.db.close()
        #HistoricalDataByDay.insert(row).execute()