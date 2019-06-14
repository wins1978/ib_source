import os

from peewee import *

from playhouse.db_url import connect
from common import *
import settings
settings.init()

from pika_mq import *

# Connect to the database URL defined in the environment, falling
# back to a local Sqlite database if no database URL is specified.
# mysql://user:passwd@ip:port/my_db

def main():
    SetupLogger()
    logging.info("STARTING DATA COLLECTING...")

    try:
        settings.db.connect()
        mq = PikaMQ()
        mq.start_consuming()
    except:
        raise
    finally:
        print("close db and mq at END")
        mq.stop_consuming()
        settings.db.close()
        logging.error("END")

if __name__ == "__main__":
    main()