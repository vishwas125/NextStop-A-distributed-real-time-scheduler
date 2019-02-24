import pandas as pd
import datetime
import _thread
import time

# Define a function for the thread
def print_lat_lan( filename, delay):
   geocordinates = pd.readcsv("filename")
   for i in geocordinates:
     time.sleep(delay)
     print ("%s: %s" % ({"Eid": (geocordinates[0], geocordinates[1])}))

# Create two threads as follows
try:
  _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
  _thread.start_new_thread( print_time, ("Thread-2", 2, ) )
except:
  print ("Error: unable to start thread")

while 1:
  pass`