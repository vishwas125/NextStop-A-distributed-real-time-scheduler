from ServiceLayer.Scheduler import Scheduler
from StreamingSystem.CosumerService import consume_location_data


class OptumServer:
    def consume_location_data_and_schedule_tasks(self, location_data):
        # location_data = consume_location_data() // Kafka cosumer not working

        for data in location_data:
            scheduler = Scheduler()
            scheduler.logData(data)
            scheduler.fetchPrioritizedTasks()
            scheduler.check_candidacy()
