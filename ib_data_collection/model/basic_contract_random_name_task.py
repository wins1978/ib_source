from peewee import *
import settings

class BasicContractRandomNameTask(Model):
    id = AutoField()
    task_name = CharField(max_length=50)
    task_status = CharField(default='DONE')
    last_update_time = DateField()

    class Meta:
        database = settings.db
        table_name = 'basic_contract_random_name_task'