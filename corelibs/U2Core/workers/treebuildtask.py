class TreeBuildTask:

    def __init__(self, alignment):
        self.alignment = alignment
        self.result = None
        self.finished = False

    def run(self):

        self.result = "(A,B,C);"

        self.finished = True