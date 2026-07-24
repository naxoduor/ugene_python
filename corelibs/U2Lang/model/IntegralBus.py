from message import Message
from bus_map import BusMap

class IntegralBus:

    def __init__(self, port):

        self.port = port

        self.bus_map = BusMap()

        self.channels = []

        self.context = {}

        self.complement = None

    def add_channel(self, channel):

        self.channels.append(channel)

    def add_complement(self, bus):

        self.complement = bus

    def put(self, message):

        mapped = Message(
            self.bus_map.compose(message),
            message.metadata
        )

        for channel in self.channels:
            channel.put(mapped)

    def get(self):

        if not self.channels:
            return None

        msg = self.channels[0].get()

        reduced = self.bus_map.reduce(msg)

        return Message(reduced, msg.metadata)

    def has_message(self):

        if not self.channels:
            return 0

        return min(ch.has_message() for ch in self.channels)

    def is_ended(self):

        return any(ch.is_ended() for ch in self.channels)