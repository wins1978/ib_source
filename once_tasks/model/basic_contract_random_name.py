from peewee import *
import settings

class BasicContractRandomName(Model):
    id = AutoField()
    name = CharField(max_length=10)
    last_update_date = DateField(index=True)

    class Meta:
        database = settings.db
        table_name = 'basic_contract_random_name'