# Assuming the following classes exist
# class AssemblyConsensusAlgorithmFactory:
#     def get_id(self) -> str:
#         pass
#
# class AssemblyConsensusAlgorithmFactoryDefault(AssemblyConsensusAlgorithmFactory):
#     ...
#
# class AssemblyConsensusAlgorithmFactorySamtools(AssemblyConsensusAlgorithmFactory):
#     ...

class AssemblyConsensusAlgorithmRegistry:
    def __init__(self):
        self.algorithms = {}
        self.add_algorithm_factory(AssemblyConsensusAlgorithmFactoryDefault())
        self.add_algorithm_factory(AssemblyConsensusAlgorithmFactorySamtools())

    def get_algorithm_factory(self, algo_id: str):
        """Return the algorithm factory for the given ID, or None if not found."""
        return self.algorithms.get(algo_id)

    def add_algorithm_factory(self, algo):
        """Add a new algorithm factory, replacing any existing factory with the same ID."""
        algo_id = algo.get_id()
        old_version = self.algorithms.get(algo_id)
        if old_version is not None:
            # Explicitly delete reference if needed (Python GC handles memory)
            del old_version
        self.algorithms[algo_id] = algo

    def __del__(self):
        """Destructor to clear all algorithm factories."""
        # Not strictly necessary in Python due to garbage collection
        self.algorithms.clear()