import os
from peewee import *
from playhouse.db_url import connect

def init():
    global db 
    db= connect(os.environ.get('PROD_DATABASE')) 
    
    global byday_data_list
    byday_data_list = []