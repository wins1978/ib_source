from peewee import *

global db 
db= connect(os.environ.get('MY_DATABASE'))
