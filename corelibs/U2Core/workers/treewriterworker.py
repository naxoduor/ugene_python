class TreeWriterWorker(Actor):

    def __init__(self):

        super().__init__()

        self.input_ports["in"] = Port()

    def init(self):
        print("Writer initialized")

    def tick(self):

        if not self.input_ports["in"].has_message():
            return

        tree = self.input_ports["in"].get()

        print("Writing tree:")
        print(tree.data)

        self.finished = True