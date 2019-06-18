from peewee import *
import settings

class BasicContractInfo(Model):
    id = AutoField()
    symbol = CharField(max_length=64)
    sec_type = CharField(max_length=20)
    currency = CharField(max_length=10)
    exchange = CharField(max_length=30)
    primary_exchange = CharField(max_length=30)
    last_byday_import_date = DateTimeField()
    disabled = DateTimeField(default="N")
    publish_time = DateTimeField()
    create_time = DateTimeField()

    class Meta:
        database = settings.db
        table_name = 'basic_contract_info'