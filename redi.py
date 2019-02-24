import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
Eid = "123"
r.sadd(Eid+'value', "10,20")
r.sadd(Eid+'task', 'T1')
print(list(r.smembers(Eid+'value')))