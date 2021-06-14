import json

from parse import Culture
import time
import pika
from config import RABBIT_HOST, RABBIT_PORT, RABBIT_QUEUE

#TODO Парсить поле Event
#TODO Разобраться с временем события
#TODO Тэги



def connect_rabbit_queue(fn):
    def wrapped():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT))
        channel = connection.channel()
        channel.queue_declare(queue=RABBIT_QUEUE)
        fn(channel)
        connection.close()

    return wrapped


# @connect_rabbit_queue
def send_queue():
    cult = Culture()
    cult.get_events()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT))
    channel = connection.channel()
    channel.queue_declare(queue=RABBIT_QUEUE)
    for event in cult.events:
        message = json.dumps(event.dict())
        channel.basic_publish(exchange='', routing_key=RABBIT_QUEUE, body=message.encode())
    connection.close()

def app_run():
    while True:
        send_queue()
        time.sleep(300)


if __name__ == '__main__':
    app_run()