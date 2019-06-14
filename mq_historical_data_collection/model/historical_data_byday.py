from peewee import *
import settings

class HistoricalDataByDay(Model):
    id = AutoField()
    symbol = CharField()
    req_id = IntegerField()
    stock_time = DateField()
    stock_time_str = CharField()
    open_pri = DecimalField()
    high_pri = DecimalField()
    low_pri = DecimalField()
    close_pri = DecimalField()

    class Meta:
        table_name = 'historical_data_byday'
    class Meta:
        database = settings.db