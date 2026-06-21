class MolecularSurfaceFactoryRegistry:
    def __init__(self, p_own=None):
        self._p_own = p_own
        self.surf_map = {}

        # equivalent to registerSurfaceFactory(new VanDerWaalsSurfaceFactory(), "vdWS");
        self.register_surface_factory(VanDerWaalsSurfaceFactory(), "vdWS")

    def register_surface_factory(self, surf, surf_id: str) -> bool:
        if surf_id in self.surf_map:
            return False
        self.surf_map[surf_id] = surf
        return True

    def had_registered(self, surf_id: str) -> bool:
        return surf_id in self.surf_map

    def get_surface_factory(self, surf_id: str):
        return self.surf_map.get(surf_id, None)

    def get_surf_name_list(self):
        return list(self.surf_map.keys())