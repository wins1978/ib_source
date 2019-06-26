import pika

class PikaMQ:
    def __init__(self):
        print("init mq...")
        self.mq_conn = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.mq_conn.channel()
        self.channel.queue_declare(queue='ib_historical_data_byday')

    def send(self,msg):
        self.channel.basic_publish(exchange='ib_historical_data_byday', routing_key='ib_historical_data_byday', body=msg)

    def close(self):
        print("closing mq")
        self.mq_conn.close()

