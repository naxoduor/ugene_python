class ReadFastaWorker(Actor):

    def __init__(self, fasta_file):
        super().__init__()

        self.fasta_file = fasta_file

        self.output_ports["out"] = Port()

        self.loaded = False

    def init(self):
        print("Reader initialized")

    def tick(self):

        if self.loaded:
            self.finished = True
            return

        sequences = [
            "ATGCGA",
            "ATGCAA",
            "ATGCCA"
        ]

        self.output_ports["out"].put(
            Message(sequences)
        )

        self.loaded = True