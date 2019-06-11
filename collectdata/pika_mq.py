import pika

class PikaMQ:
    def __init__(self):
        print("init mq...")
        self.mq_conn = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.mq_conn.channel()
        self.channel.queue_declare(queue='ib_historical_data_byday')

        self.channel.basic_consume(
            queue='ib_historical_data_byday', on_message_callback=self.callback, auto_ack=True)

    def start_consuming(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def callback(self,ch, method, properties, body):
        msg = body.decode()
        arr = msg.split(",")
        for item in arr:
            print(item.strip())

    def stop_consuming(self):
        self.channel.stop_consuming('ib_historical_data_byday')