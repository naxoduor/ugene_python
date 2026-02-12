from threading import Lock


class SmithWatermanTaskFactoryRegistry:
    def __init__(self, owner=None):
        self._owner = owner
        self._factories = {}
        self._lock = Lock()

    def __del__(self):
        # Optional cleanup; Python GC handles most cases.
        # If factories need explicit cleanup, do it here.
        self._factories.clear()

    def register_factory(self, factory, factory_id):
        with self._lock:
            if factory_id in self._factories:
                return False
            self._factories[factory_id] = factory
            return True

    def get_factory(self, factory_id):
        return self._factories.get(factory_id, None)

    def get_list_factory_names(self):
        return list(self._factories.keys())

    def had_registered(self, factory_id):
        return factory_id in self._factories