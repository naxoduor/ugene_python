class Port:
    def __init__(self):
        self.queue = []

    def put(self, msg):
        self.queue.append(msg)

    def get(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def has_message(self):
        return len(self.queue) > 0


class Actor:
    def __init__(self):
        self.input_ports = {}
        self.output_ports = {}
        self.finished = False

    def init(self):
        pass

    def tick(self):
        pass