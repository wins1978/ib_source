from peewee import *
import settings

class HistoricalDataByDay(Model):
    id = AutoField()
    vendor_name = CharField()
    tel = CharField()
    contact_name = CharField()
    cost_alert = BitField()
    need_cost_advance = CharField()
    is_valid = CharField()

    class Meta:
        table_name = 'historical_data_byday'
    class Meta:
        database = settings.db