import threading, logging, time
import multiprocessing
import pandas as pd
import datetime
import _thread
import time
from kafka import KafkaConsumer, KafkaProducer
import redis

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "localhost"
redis_port = 6379
redis_password = ""

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    # Define a function for the thread
    def print_lat_lan(filename, delay):
        geocordinates = pd.readcsv("filename")
        for i in geocordinates:
            time.sleep(delay)
            print("%s: %s" % ({"Eid": (geocordinates[0], geocordinates[1])}))


    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        while not self.stop_event.is_set():
            producer.send('test', b"test")
            producer.send('test', b"\xc2Hola, pavan unnu eda!")
            # Create two threads as follows
            # try:
            #     _thread.start_new_thread(print_lat_lan("filename", 2,))
            #     _thread.start_new_thread(print_lat_lan("filename", 2,))
            # except:
            #     print("Error: unable to start thread")
            # time.sleep(1)

        producer.close()



class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe(['test'])

        while not self.stop_event.is_set():
            for message in consumer:
                try:

                    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
                    # using the default encoding utf-8.  This is client specific.
                    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

                    # step 4: Set the hello message in Redis
                    r.set("msg:hello", message)

                    # step 5: Retrieve the hello message from Redis
                    msg = r.get("msg:hello")
                    print(msg)

                except Exception as e:
                    print(e)
                if self.stop_event.is_set():
                    break


        consumer.close()


def main():
    tasks = [
        Producer(),
        Consumer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)

    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()