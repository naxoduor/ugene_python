class MsaConsensusAlgorithmFactoryDefault():
    def __init__(self):
        

        self.name = tr("Default")
        self.description = tr(
            "Based on JalView algorithm. Returns '+' if there are 2 characters "
            "with high frequency. Returns symbol in lower case if the symbol "
            "content in a row is lower than the threshold specified."
        )

        self.minThreshold = 1
        self.maxThreshold = 100
        self.defaultThreshold = 100
        self.thresholdSuffix = "%"

    def create_algorithm(self, msa, ignore_trailing_leading_gaps):
        return MsaConsensusAlgorithmDefault(self, ignore_trailing_leading_gaps)


