from StreamingSystem.StreamingService import Consumer


def consume_location_data():
    # Stream the location data to the kafak consumer according to the pings
    consumer = Consumer()
    location_data = consumer.consume_real_time_pings()
    print("Events is Consumed : ", location_data)
    return location_data
