class StructuralAlignmentAlgorithmRegistry(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.factories = {}

    def __del__(self):
        # In Python, explicit deletion is usually unnecessary,
        # but kept here to mirror C++ ownership semantics.
        self.factories.clear()

    def registerAlgorithmFactory(self, factory, id_str):
        assert id_str not in self.factories
        self.factories[id_str] = factory

    def getAlgorithmFactory(self, id_str):
        return self.factories.get(id_str, None)

    def getFactoriesIds(self):
        return list(self.factories.keys())

    def createStructuralAlignmentAlgorithm(self, algorithm):
        factory = self.getAlgorithmFactory(algorithm)
        return factory.create() if factory else None

    def createStructuralAlignmentTask(self, algorithm, settings):
        factory = self.getAlgorithmFactory(algorithm)
        return StructuralAlignmentTask(factory.create(), settings) if factory else None