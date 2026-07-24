from corelibs.U2Lang.model.message import Message
from base_worker import BaseWorker

class UpperCaseWorker(BaseWorker):

    def tick(self):

        input_bus = self.buses["input"]

        output_bus = self.buses["output"]

        if input_bus.has_message() == 0:
            return

        msg = input_bus.get()

        text = msg.data["text"]

        result = Message({
            "text": text.upper()
        })

        output_bus.put(result)


from message import Message
from base_worker import BaseWorker

class UpperCaseWorker(BaseWorker):

    def tick(self):

        input_bus = self.buses["input"]
        output_bus = self.buses["output"]

        if input_bus.has_message() == 0:
            return

        msg = input_bus.get()

        text = msg.data["text"]

        result = Message({
            "text": text.upper()
        })

        output_bus.put(result)