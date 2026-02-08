class MsaDistanceAlgorithmRegistry:
    def __init__(self):
        # Dictionary to store algorithms by their ID
        # Key: algorithm ID (str), Value: algorithm factory object
        self.algorithms = {}

    def add_algorithm(self, algo):
        """
        Adds an algorithm factory to the registry.
        If an algorithm with the same ID already exists, it is replaced.
        """
        algo_id = algo.get_id()
        if algo_id in self.algorithms:
            # In C++ code, oldVersion was deleted; in Python we just replace it
            old_version = self.algorithms[algo_id]
            # If needed, you could clean up old_version here
        self.algorithms[algo_id] = algo

    def get_algorithm_ids(self):
        """
        Returns a list of all registered algorithm IDs.
        """
        return [algo.get_id() for algo in self.algorithms.values()]
