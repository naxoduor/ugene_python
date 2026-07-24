from integral_bus import IntegralBus

class BaseWorker:

    def __init__(self, actor, auto_transit=True):

        self.actor = actor

        self.process_done = False

        self.buses = {}

        for port in actor.get_ports():

            bus = IntegralBus(port)

            self.buses[port.name] = bus

            port.set_peer(bus)

        if auto_transit:

            for inp in actor.input_ports:

                in_bus = inp.get_peer()

                for out in actor.output_ports:

                    out_bus = out.get_peer()

                    out_bus.add_complement(in_bus)

                    in_bus.add_complement(out_bus)

    def tick(self):
        raise NotImplementedError