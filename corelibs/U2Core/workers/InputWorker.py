from message import Message
from base_worker import BaseWorker

class InputWorker(BaseWorker):

    def tick(self):

        output_bus = self.buses["output"]

        msg = Message({
            "text": "hello ugene"
        })

        output_bus.put(msg)