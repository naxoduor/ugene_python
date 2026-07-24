from queue import Queue

class CommunicationChannel:

    def __init__(self):
        self.queue = Queue()
        self.ended = False

    def put(self, message):
        self.queue.put(message)

    def get(self):
        return self.queue.get()

    def look(self):
        if self.queue.empty():
            return None

        message = self.queue.get()
        self.queue.put(message)
        return message

    def has_message(self):
        return self.queue.qsize()

    def has_room(self):
        return 1000 - self.queue.qsize()

    def set_ended(self):
        self.ended = True

    def is_ended(self):
        return self.ended