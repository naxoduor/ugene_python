from PyQt5.QtCore import QObject
# or: from PySide6.QtCore import QObject


class MsaDistanceAlgorithmFactoryHammingRevCompl(MsaDistanceAlgorithmFactory):

    def __init__(self, parent=None):
        super().__init__(
            BuiltInDistanceAlgorithms.HAMMING_REVCOMPL_ALGO,
            DistanceAlgorithmFlag_Nucleic,
            parent
        )

    def getDescription(self) -> str:
        return self.tr("Based on Hamming distance between two sequences")

    def getName(self) -> str:
        return self.tr("Hamming reverse-complement")

    def createAlgorithm(self, ma: Msa, parent: QObject = None) -> MsaDistanceAlgorithm:
        return MsaDistanceAlgorithmHammingRevCompl(self, ma)
