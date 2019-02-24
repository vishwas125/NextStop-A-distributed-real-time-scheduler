from ServiceLayer.OptumClients import OptumClients
from ServiceLayer.OptumServer import OptumServer
import _thread


class Hack_Illinois_2019:

    def simulate(self):
        client = OptumClients()
        server = OptumServer()

        client.run_client()
        # server.consume_location_data_and_schedule_tasks();

        # my_server = _thread.start_new(server.consume_location_data_and_schedule_tasks())
        #
        # my_client = _thread.start_new(client.run_client())


if __name__ == '__main__':
    we_hacked_it = Hack_Illinois_2019()
    we_hacked_it.simulate()
