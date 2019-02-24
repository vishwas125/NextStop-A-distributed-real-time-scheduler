from kafka import KafkaConsumer
from json import loads
import redis
redis_host = "localhost"
redis_port = 6379
redis_password = ""
consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
consumer.subscribe(['test'])

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


consumer.close()


