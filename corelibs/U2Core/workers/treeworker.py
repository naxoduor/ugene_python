class TreeWorker(Actor):

    def __init__(self):

        super().__init__()

        self.input_ports["in"] = Port()
        self.output_ports["out"] = Port()

        self.task = None

    def init(self):
        print("Tree worker initialized")

    def tick(self):

        if self.task is None:

            if not self.input_ports["in"].has_message():
                return

            msg = self.input_ports["in"].get()

            self.task = TreeBuildTask(
                msg.data
            )

            self.task.run()

        if self.task.finished:

            self.output_ports["out"].put(
                Message(self.task.result)
            )

            self.finished = True