class MsaDistanceAlgorithmFactoryHamming():
    
    def getDescription(self):
        return self.tr("Based on Hamming distance between two sequences")

    def getName(self):
        return self.tr("Hamming dissimilarity")

    def createAlgorithm(self, ma, parent=None):
        res = MsaDistanceAlgorithmHamming(self, ma)


        return res
