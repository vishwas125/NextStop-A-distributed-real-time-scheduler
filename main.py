import sys
import collections
import redis
import sqlite3
from sqlite3 import Error
from collections import deque
import datetime
from geopy.geocoders import Nominatim
import googlemaps
import time
import struct

geolocator = Nominatim(user_agent="specify_your_app_name_here")
gmaps = googlemaps.Client(key='AIzaSyAgfpS97gZA3mp75ho1_ecO0M7adSDqhAE')


class Scheduler():

    def __init__(self):

        # global data
        self.logdataFile = ''
        self.companyDBfile = ''
        self.lat = 0.0
        self.lon = 0.0
        self.empId = 0
        self.queue = deque()
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        # self.r.flushall()
        self.con = self.create_connection('/Users/amoghvenkatesh/PycharmProjects/HackIllinois2019/venv/hackillinois.db')
        # print("Initialized")

    # method to log live location of the nurse - stores into the DB
    def logData(self, data):
        self.empId = list(data.keys())[0]
        key = str(datetime.time)

        # print('existing', self.r.smembers(str(self.empId) + 'starttime'))

        redis_value = self.r.exists(str(self.empId) + 'starttime')
        print(redis_value)
        epoch_time = str(time.time())

        print("eph:", epoch_time)

        if redis_value == 0:
            self.r.set(str(self.empId) + 'starttime', epoch_time)

        self.lat = (data[self.empId])[0]
        self.lon = (data[self.empId])[1]
        #con = self.create_connection(self.companyDBfile)
        cur = self.con.cursor()
        try:
            cur.execute('Insert into DATALOG values(?,?,?,?)', self.empId, self.lat, self.lon, 'now')
        except:
            return False

        return True

    # get the tasks, filter by due date and order by priority; store in a deque for easy ops
    def fetchPrioritizedTasks(self):

        cur = self.con.cursor()
        try:
            # rows=cur.execute('select * from TASK_DATA')
            # for x in rows:
            #     print(x)
            res=cur.execute('select task_id from TASK_DATA where due_date = strftime("%m/%d/%Y", date("now")) ORDER BY CASE priority_level WHEN "Low" THEN 3 WHEN "Medium" THEN 2 WHEN "High" THEN 1 END;').fetchall()

            
            # con.commit()

            #ids = cur.fetchall()

            for x in res:
                self.queue.append(x)

        except:
            return False

        return True

    def checkassignment(self):
        curlocation = self.r.get(self.empId + 'cur-location')
        if [self.lat, self.lon] == [float(x) for x in curlocation.split(",")]:
            val = self.r.get(self.empId + 'wait-counter')
            if val >= 4:
                self.reassign()
                return
            r.set(self.empId + 'wait-counter', val + 1)

    def check_candidacy(self):
        #con = self.create_connection(self.companyDBfile)
        cur = self.con.cursor()
        curtime = str(time.time())
        # if not starttime:
        #     r.set(str(empId)+'starttime', curtime)
        #     starttime = r.get()(str(self.empId)+'starttime')
        # print(r.get()(str(self.empId)+'starttime'))

        # checking for total time and count of tasks
        completedtaskcur = cur.execute('SELECT count(*) FROM  TASK_ASSIGNED GROUP BY employee_id;')
        temp = completedtaskcur.fetchall()

        if temp:
            completedtask = temp[0]

        else:
            completedtask = 0

        curtask = (self.r.get(str(self.empId) + 'curtask'))

        if curtask:
            return

        curtask = 1

        starttime = self.r.get(str(self.empId) + 'starttime')

        # check the feasibility if the candidate is avaialble to take up the wor
        if not completedtask + curtask > 3 or not int(curtime) - int(starttime) >= 8 * 60 * 60 * 100:
            task_time = (float(curtime) - float(starttime))/(60*60*1000)
            task = self.check_feasibility(task_time)
            print(task)
            if task != None:
                # assigning the task
                # print(Eid,"assigned",task)
                r.set(self.empId + 'curtask', task)

                print("TASK ASSIGNED:", task)

    def reassign(self):
        taskid = self.r.get(self.empId + 'curtask')
        self.r.delete(self.empId + 'curtask')
        # update the priority queue
        self.queue.appendleft(taskid)

    def check_feasibility(self, remaining_employee_shift_time):
        # get employee's current address
        #     emp_latitude, emp_longitude = get_employee_current_ping(emp_id)

        # get queue top_element
        top = 0
        # get task id of top element of queue
        while (self.queue):
            task_id = self.queue.popleft()
            patient_address, treatment_time = self.get_patient_address(task_id)
            p_lat, p_lon = self.compute_patient_latLong(patient_address)
            travel_time = self.compute_eta((self.lat, self.lon), (p_lat, p_lon))
            if travel_time + treatment_time <= remaining_employee_shift_time:
                return task_id
        return None

    def get_employee_current_ping(self, emp_id):
        pass

    def get_queue_top_element(self, top):
        return self.queue[top]

    def get_patient_address(self, t_id):
        con = self.create_connection(self.companyDBfile)
        cur = con.cursor()
        # Get address of patient given a task ID t_id
        try:
            cur.execute(
                "select pd.street_address, ttd.task_duration from TASK_DATA td inner join PATIENT_DATA pd on td.patient_id = pd.patient_id inner join TASK_TYPE_DURATION ttd on ttd.task_type_id = td.task_type_id where td.task_id = ?;",
                t_id)
            result = cur.fetchall()[0]
        except:
            return None
        return (result[0], result[1])

    def compute_patient_latLong(self, address):
        location = geolocator.geocode(address)
        return location.latitude, location.longitude

    def compute_eta(self, coords_1, coords_2):
        my_dist = \
        gmaps.distance_matrix(geolocator.reverse(coords_2).address, geolocator.reverse(coords_1).address)['rows'][0][
            'elements'][0]
        return (my_dist['duration']['text'])

    # create a connection to the database and return the con object
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return None
#
# if __name__ == '__main__':
#     scheduler = Scheduler()
#     scheduler.logData(data)
#     scheduler.fetchPrioritizedTasks()
#     scheduler.check_candidacy()
