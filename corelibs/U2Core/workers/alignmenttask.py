class AlignmentTask:

    def __init__(self, sequences):
        self.sequences = sequences
        self.result = None
        self.finished = False

    def run(self):

        self.result = [
            "ATGCGA",
            "ATGCAA",
            "ATGCCA"
        ]

        self.finished = True