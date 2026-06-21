NUM_ELEMENTS = 120  # choose a safe upper bound (adjust if needed)

atomRadiusTable = [0.0] * NUM_ELEMENTS

_initialized = False

def init_atom_constants():
    global _initialized, atomRadiusTable

    if not _initialized:
        atomRadiusTable[1] = 0.23
        atomRadiusTable[5] = 0.83
        atomRadiusTable[6] = 0.68
        atomRadiusTable[7] = 0.68
        atomRadiusTable[8] = 0.68
        atomRadiusTable[9] = 0.64
        atomRadiusTable[14] = 1.20
        atomRadiusTable[15] = 1.05
        atomRadiusTable[16] = 1.02
        atomRadiusTable[17] = 0.99
        atomRadiusTable[33] = 1.21
        atomRadiusTable[34] = 1.22
        atomRadiusTable[35] = 1.21
        atomRadiusTable[52] = 1.47
        atomRadiusTable[53] = 1.40

        _initialized = True


def get_atom_covalent_radius(atomic_number: int) -> float:
    if atomic_number < len(atomRadiusTable):
        return atomRadiusTable[atomic_number]
    return 0.0


import math
from dataclasses import dataclass
from typing import List


TOLERANCE = 1.0


@dataclass
class Vector3D:
    x: float
    y: float
    z: float


@dataclass
class Atom:
    atomic_number: int
    coord3d: Vector3D


class MolecularSurface:
    def __init__(self):
        self.faces = []

    def get_faces(self):
        return self.faces

    def find_atom_neighbors(self, a: Atom, atoms: List[Atom]) -> List[Atom]:
        neighbors = []
        max_atom_radius = 1.0
        double_radius = 2 * max_atom_radius

        v1 = a.coord3d

        for neighbor in atoms:
            if neighbor is a:
                continue

            v2 = neighbor.coord3d

            if (abs(v1.x - v2.x) <= double_radius and
                abs(v1.y - v2.y) <= double_radius and
                abs(v1.z - v2.z) <= double_radius):
                neighbors.append(neighbor)

        return neighbors

    def get_atom_surface_dots(self, a: Atom, detail_level: int):
        radius = TOLERANCE + get_atom_covalent_radius(a.atomic_number)
        return GeodesicSphere(a.coord3d, radius, detail_level)

    def vertex_neighbours_one_of(self, v: Vector3D, atoms: List[Atom]) -> bool:
        for a in atoms:
            r = get_atom_covalent_radius(a.atomic_number) + TOLERANCE

            dx = v.x - a.coord3d.x
            dy = v.y - a.coord3d.y
            dz = v.z - a.coord3d.z

            if dx*dx + dy*dy + dz*dz <= r * r:
                return True

        return False

    def estimate_memory_usage(self, number_of_atoms: int) -> int:
        import sys
        max_int = 2**31 - 1
        return max_int * 8 * 6  # double ~= 8 bytes