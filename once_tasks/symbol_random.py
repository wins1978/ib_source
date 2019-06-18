import os
import datetime

from peewee import *

from common import *
import settings
from model.basic_contract_random_name import BasicContractRandomName

class SymbolRandom:
    def createRandomSymbolOnceTime(self):
        print("running createRandomSymbolOnceTime")
        names = GetSymbolName()
        idx = 1
        for name in names:
            self._saveData(name)
            idx = idx +1
            # print(idx)
    
    def _saveData(self,name):
        #cursor = settings.db.cursor()
        try:
            BasicContractRandomName.create(name=name,
                    last_update_date=datetime.datetime.now())
            # time = datetime.datetime.now()
            # sql = "insert into basic_contract_random_name( \
            #     name, last_update_date) \
            #     values ('%s','%s') " % \
            #     (name,time)
            # cursor.execute(sql)
            # settings.db.commit()
        except Exception as e:
            print(e)
            #settings.db.rollback()