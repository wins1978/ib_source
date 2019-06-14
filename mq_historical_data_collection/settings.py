import os
from peewee import *
from playhouse.db_url import connect

def init():
    global db 
    db= connect(os.environ.get('MY_DATABASE')) 
    
    global byday_data_list
    byday_data_list = []