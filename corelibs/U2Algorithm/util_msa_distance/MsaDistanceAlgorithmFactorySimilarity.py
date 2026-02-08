class MsaDistanceAlgorithmFactorySimilarity(MsaDistanceAlgorithmFactory):
    def get_description(self) -> str:
        return "Based on similarity distance between two sequences"

    def get_name(self) -> str:
        return "Similarity"

    def create_algorithm(self, ma: 'Msa', parent=None) -> 'MsaDistanceAlgorithm':
        res = MsaDistanceAlgorithmSimilarity(self, ma)
        return res
