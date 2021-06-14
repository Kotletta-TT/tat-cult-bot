import pika
import json
import csv
import time

#TODO Делать запросы и сверять site_id для исключения дублей

from config import RABBIT_QUEUE, RABBIT_HOST, RABBIT_PORT
from models import Event, Base, Facts
from db_helper import Session, engine

session = Session()

Base.metadata.create_all(engine)
time.sleep(15)
with open('facts.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        fact = Facts(**row)
        session.add(fact)
        session.commit()

def queue_to_db():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT))
    channel = connection.channel()
    channel.queue_declare(queue=RABBIT_QUEUE)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        tmp = session.query(Event).filter_by(site_id=message['site_id']).first()
        if tmp and tmp.site_id == message['site_id']:
            print(f"This row in DB, site_id:{tmp.site_id}")
        else:
            try:
                event = Event(**message)
                session.add(event)
                session.commit()
            except Exception as e:
                print(e)
            ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue=RABBIT_QUEUE, on_message_callback=callback)
    channel.start_consuming()


def app_run():
    queue_to_db()


if __name__ == '__main__':
    app_run()