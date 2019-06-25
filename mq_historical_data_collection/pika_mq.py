import functools
import logging
import pika
import threading
import time
import os
import datetime
import settings
from historical_data_byday_imp import HistoricalDataByDayImp

# https://github.com/pika/pika/blob/0.12.0/examples/basic_consumer_threaded.py
def ack_message(channel, delivery_tag):
    """Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass

def do_work(connection, channel, delivery_tag, body):
    thread_id = threading.get_ident()
    fmt1 = 'Thread id: {} Delivery tag: {} Message body: {}'
    msg = fmt1.format(thread_id, delivery_tag, body)
    #logging.info(msg)
    HistoricalDataByDayImp.receiveData(body)
    # Sleeping to simulate 10 seconds of work
    #time.sleep(10)
    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)

def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(connection, channel, delivery_tag, body))
    t.start()
    threads.append(t)
    
def monitorTime():
    exitApp("18:30:00","18:40:00")
    timer = threading.Timer(100,monitorTime)
    timer.start()

def exitApp(startTimeStr,endTimeStr):
    # "16:00:00","17:30:00"
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    
    targetStartTimeStr = dt + " " + startTimeStr
    targetStartTime = datetime.datetime.strptime(targetStartTimeStr, "%Y-%m-%d %H:%M:%S")
    
    targetEndTimeStr = dt + " " + endTimeStr
    targetEndTime = datetime.datetime.strptime(targetEndTimeStr, "%Y-%m-%d %H:%M:%S")
    
    currentTime = datetime.datetime.now()
    
    if currentTime >= targetStartTime and currentTime < targetEndTime :
        logging.info("exit at: %s" %currentTime)
        print("exit at: %s" %currentTime)
        os._exit(0)        
    
# credentials = pika.PlainCredentials('guest', 'guest')
# Note: sending a short heartbeat to prove that heartbeats are still
# sent even though the worker simulates long-running work
parameters =  pika.ConnectionParameters('localhost', heartbeat=5)
#parameters =  pika.ConnectionParameters('localhost', credentials=credentials, heartbeat=5)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange="ib_historical_data_byday", exchange_type="direct", passive=False, durable=True, auto_delete=False)
channel.queue_declare(queue="ib_historical_data_byday")
channel.queue_bind(queue="ib_historical_data_byday", exchange="ib_historical_data_byday", routing_key="ib_historical_data_byday")
# Note: prefetch is set to 1 here as an example only and to keep the number of threads created
# to a reasonable amount. In production you will want to test with different prefetch values
# to find which one provides the best performance and usability for your solution
channel.basic_qos(prefetch_count=1)

threads = []
on_callback = functools.partial(on_message, args=(connection, threads))
channel.basic_consume(queue='ib_historical_data_byday', on_message_callback=on_callback)
try:
    monitorTime()
    channel.start_consuming()
    
except KeyboardInterrupt:
    channel.stop_consuming()

# Wait for all to complete
for thread in threads:
    thread.join()

connection.close()