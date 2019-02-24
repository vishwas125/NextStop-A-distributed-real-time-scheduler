import threading, logging, time
import multiprocessing
import pandas as pd
import datetime
import _thread
import time
from kafka import KafkaConsumer, KafkaProducer
import redis
from main import Scheduler

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "localhost"
redis_port = 6379
redis_password = ""

class Producer():

    # Define a function for the thread
    def print_lat_lan(self):


        # Wrapper for producer here

        produce_real_time_pings()

        geocordinates = pd.read_csv("sample_coordinates.csv")
        for i in range(len(geocordinates)):
            print(geocordinates.iloc[i]['latitude'],geocordinates.iloc[i]['Route_id'],geocordinates.iloc[i]['longitude'])
            data = {str(geocordinates.iloc[i]['Route_id']): (geocordinates.iloc[i]['latitude'], geocordinates.iloc[i]['longitude'])}



           '''
           The following lines of code simulates the consumer : A kafka consumer is implemented 
           
           '''
            # wrapper for consumer here . write to common DB to fetch the data

            scheduler = Scheduler()
            scheduler.logData(data)
            scheduler.fetchPrioritizedTasks()
            scheduler.check_candidacy()


if __name__ == "__main__":
    producer = Producer()
    producer.print_lat_lan()