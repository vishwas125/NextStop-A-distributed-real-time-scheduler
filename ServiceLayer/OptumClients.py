import pandas as pd

from ServiceLayer.OptumServer import OptumServer
from ServiceLayer.Scheduler import Scheduler

# step 2: define our connection information for Redis
# Replaces with your configuration information
from StreamingSystem.ProducerService import produce_real_time_pings

redis_host = "localhost"
redis_port = 6379
redis_password = ""


class OptumClients:
    def run_client(self):
        my_server = OptumServer()
        geocordinates = pd.read_csv(
            "/Users/amoghvenkatesh/PycharmProjects/HackIllinois2019/DataLayer/sample_coordinates.csv")

        for i in range(len(geocordinates)):
            location_data = {str(geocordinates.iloc[i]['Route_id']): (
                geocordinates.iloc[i]['latitude'], geocordinates.iloc[i]['longitude'])}
            # produce_real_time_pings(location_data)  # produces kafka events
            my_server.consume_location_data_and_schedule_tasks([location_data])
