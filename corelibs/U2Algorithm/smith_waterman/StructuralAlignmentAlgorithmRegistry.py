# namespace U2 (Python module style)

class StructuralAlignmentAlgorithmRegistry:
    def __init__(self, parent=None):
        # `parent` kept for API similarity; not used in Python
        self.parent = parent
        self.factories = {}

    def register_algorithm_factory(self, factory, id_):
        assert id_ not in self.factories, f"Factory with id '{id_}' already registered"
        self.factories[id_] = factory

    def get_algorithm_factory(self, id_):
        return self.factories.get(id_, None)

    def get_factories_ids(self):
        return list(self.factories.keys())
      
    def create_structural_alignment_algorithm(self, algorithm):
        factory = self.get_algorithm_factory(algorithm)
        if factory is None:
            raise KeyError(f"No factory registered for algorithm '{algorithm}'")
        return factory.create()

    def create_structural_alignment_task(self, algorithm, settings):
        factory = self.get_algorithm_factory(algorithm)
        if factory is None:
            raise KeyError(f"No factory registered for algorithm '{algorithm}'")
        return StructuralAlignmentTask(factory.create(), settings)
