import os
import sys
from peewee import *

from playhouse.db_url import connect
from common import *
import settings
settings.init()

from symbol_random import SymbolRandom

# create db model
# python -m pwiz -e mysql -H localhost -p3306 -uroot -P peewee > models.py
def main():
    SetupLogger()
    businessType = sys.argv[1]
    if businessType == "":
        print("no businessType")
        return
        
    try:
        settings.db.connect()
        # nohup python main.py SymbolRandom &
        # exit
        if businessType == "SymbolRandom":
            app = SymbolRandom()
            app.createRandomSymbolOnceTime()
    except:
        raise
    finally:
        print("close db and mq at END")
        settings.db.close()
        logging.info("END")

if __name__ == "__main__":
    main()