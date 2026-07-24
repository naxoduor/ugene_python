from base_worker import BaseWorker

class OutputWorker(BaseWorker):

    def tick(self):

        input_bus = self.buses["input"]

        if input_bus.has_message() == 0:
            return

        msg = input_bus.get()

        print("Received:", msg.data["text"])