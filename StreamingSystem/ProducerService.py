from StreamingSystem.StreamingService import Producer
import json


def produce_real_time_pings(location_data):
    # Stream the location data to the kafak consumer according to the pings
    producer = Producer()
    producer.run(topic="test", event=json.dumps(location_data).encode("UTF-8"))
    print("Event is produced")
