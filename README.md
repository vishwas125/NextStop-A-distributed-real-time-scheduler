
# NextStop-A-distributed-real-time-scheduler

A generic solution to a real time task assignment applications. Given in a few constraints, the system can assign tasks
on the go in a large distributed environment based on real team events. This solution is capable of handling real time analysis of
the progress of the task and can handle reassignments as well, to the best fit of the user/organization..

We have developed the system using Apache Kafka for streaming of geolocation data from multiple clients.
We implemented the scheduling algorithm in pythonls. We use SQL databases for logging and storing assignments.
We make use of REDIS for efficient update and  fast caching and also temporary assignment of tasks. We were also able
to efficiently handle reassignment of tasks on the go using Redis and an on the go scheduling system. The system has
a robust architecture which is highly scalable and adaptable to many environments.

