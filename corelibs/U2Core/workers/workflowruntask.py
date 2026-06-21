reader = ReadFastaWorker("seq.fa")

aligner = AlignmentWorker()

tree_builder = TreeWorker()

writer = TreeWriterWorker()

connections = [
    (reader.output_ports["out"],
     aligner.input_ports["in"]),

    (aligner.output_ports["out"],
     tree_builder.input_ports["in"]),

    (tree_builder.output_ports["out"],
     writer.input_ports["in"])
]


class WorkflowRunTask:

    def __init__(self, actors, connections):

        self.actors = actors
        self.connections = connections

    def init(self):

        for actor in self.actors:
            actor.init()

    def transfer_messages(self):

        for out_port, in_port in self.connections:

            while out_port.has_message():

                msg = out_port.get()

                in_port.put(msg)

    def tick(self):

        for actor in self.actors:
            actor.tick()

        self.transfer_messages()

    def run(self):

        self.init()

        while True:

            self.tick()

            if all(a.finished for a in self.actors):
                break

        print("Workflow finished")


workflow = WorkflowRunTask(
    [
        reader,
        aligner,
        tree_builder,
        writer
    ],
    connections
)

workflow.run()