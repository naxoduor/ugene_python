from typing import Dict, Optional, List


class PhyTreeGenerator:
    """Placeholder base class for generators."""
    pass


class PhyTreeGeneratorRegistry:
    def __init__(self, pOwn=None):
        # genMap: QMap<QString, PhyTreeGenerator*> equivalent
        self.gen_map: Dict[str, PhyTreeGenerator] = {}

    def __del__(self):
        # In Python, garbage collection handles deletion,
        # but we mimic explicit cleanup behavior.
        for generator in list(self.gen_map.values()):
            del generator
        self.gen_map.clear()

    def register_phy_tree_generator(
        self,
        generator: PhyTreeGenerator,
        gen_id: str
    ) -> bool:
        if gen_id in self.gen_map:
            return False
        self.gen_map[gen_id] = generator
        return True

    def had_registered(self, gen_id: str) -> bool:
        return gen_id in self.gen_map

    def get_generator(self, gen_id: str) -> Optional[PhyTreeGenerator]:
        return self.gen_map.get(gen_id, None)

    def get_name_list(self) -> List[str]:
        return list(self.gen_map.keys())