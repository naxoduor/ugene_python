class MsaConsensusAlgorithmFactoryStrict():
    def __init__(self):
        

        self.name = self.tr("Strict")
        self.description = self.tr(
            "The algorithm returns gap character ('-') if symbol frequency "
            "in a column is lower than threshold specified."
        )

        self.minThreshold = 1
        self.maxThreshold = 100
        self.defaultThreshold = 100
        self.thresholdSuffix = "%"
        self.isSequenceLikeResultFlag = True

    def create_algorithm(self, msa, ignore_trailing_leading_gaps: bool):
        return MsaConsensusAlgorithmStrict(self, ignore_trailing_leading_gaps)
