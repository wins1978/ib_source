import os
import os
import pprint
import shlex
import subprocess
command = shlex.split("env -i bash -c 'source ~/.bash_profile && env'")
proc = subprocess.Popen(command, stdout = subprocess.PIPE)
for line1 in proc.stdout:
    line = line1.decode()
    (key, _, value) = line.partition("=")
    if value != "":
        os.environ[key] = value.replace('\n', '')
proc.communicate()

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