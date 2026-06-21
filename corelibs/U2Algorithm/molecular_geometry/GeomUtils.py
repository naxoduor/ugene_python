import math
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Vector3D:
    x: float
    y: float
    z: float

    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length == 0:
            return self
        self.x /= length
        self.y /= length
        self.z /= length
        return self

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __mul__(self, scalar: float):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __imul__(self, scalar: float):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self


@dataclass
class Face:
    v: List[Vector3D]
    n: List[Vector3D]


class GeodesicSphere:
    elementary_sphere: Optional[List[Vector3D]] = None
    current_detail_level: int = 1

    def __init__(self, center: Vector3D, radius: float, detail_level: int):
        if (GeodesicSphere.elementary_sphere is None or
                GeodesicSphere.current_detail_level != detail_level):

            GeodesicSphere.elementary_sphere = self.create_geodesic_sphere(detail_level)
            GeodesicSphere.current_detail_level = detail_level

        base = GeodesicSphere.elementary_sphere

        vertices = [Vector3D(v.x, v.y, v.z) for v in base]
        normals: List[Vector3D] = []

        self.vertices: List[Vector3D] = vertices
        self.faces: List[Face] = []

        size = len(vertices)

        for i in range(size):
            vertex = self.vertices[i]
            vertex.normalize()
            normals.append(Vector3D(vertex.x, vertex.y, vertex.z))

            vertex *= radius
            vertex += center

        for i in range(0, size, 3):
            face = Face(
                v=[
                    self.vertices[i],
                    self.vertices[i + 1],
                    self.vertices[i + 2],
                ],
                n=[
                    normals[i],
                    normals[i + 1],
                    normals[i + 2],
                ],
            )
            self.faces.append(face)

    @staticmethod
    def interpolate(v1, v2, v3, out: List[Vector3D], detail_level: int):
        if detail_level == 0:
            out.append(v1)
            out.append(v2)
            out.append(v3)
            return

        nv1 = Vector3D((v1.x + v2.x) / 2, (v1.y + v2.y) / 2, (v1.z + v2.z) / 2)
        nv2 = Vector3D((v2.x + v3.x) / 2, (v2.y + v3.y) / 2, (v2.z + v3.z) / 2)
        nv3 = Vector3D((v3.x + v1.x) / 2, (v3.y + v1.y) / 2, (v3.z + v1.z) / 2)

        GeodesicSphere.interpolate(nv1, nv2, nv3, out, detail_level - 1)
        GeodesicSphere.interpolate(v1, nv1, nv3, out, detail_level - 1)
        GeodesicSphere.interpolate(nv1, v2, nv2, out, detail_level - 1)
        GeodesicSphere.interpolate(nv3, nv2, v3, out, detail_level - 1)

    @staticmethod
    def create_geodesic_sphere(detail_level: int) -> List[Vector3D]:
        base = [Vector3D(0, 0, 0) for _ in range(24)]

        # up
        base[0] = Vector3D(-1.0, 0.0, 0.0)
        base[1] = Vector3D(0.0, 1.0, 0.0)
        base[2] = Vector3D(0.0, 0.0, -1.0)

        base[3] = Vector3D(0.0, 0.0, -1.0)
        base[4] = Vector3D(0.0, 1.0, 0.0)
        base[5] = Vector3D(1.0, 0.0, 0.0)

        base[6] = Vector3D(1.0, 0.0, 0.0)
        base[7] = Vector3D(0.0, 1.0, 0.0)
        base[8] = Vector3D(0.0, 0.0, 1.0)

        base[9] = Vector3D(0.0, 0.0, 1.0)
        base[10] = Vector3D(0.0, 1.0, 0.0)
        base[11] = Vector3D(-1.0, 0.0, 0.0)

        # down
        base[12] = Vector3D(-1.0, 0.0, 0.0)
        base[13] = Vector3D(0.0, 0.0, -1.0)
        base[14] = Vector3D(0.0, -1.0, 0.0)

        base[15] = Vector3D(0.0, 0.0, -1.0)
        base[16] = Vector3D(1.0, 0.0, 0.0)
        base[17] = Vector3D(0.0, -1.0, 0.0)

        base[18] = Vector3D(1.0, 0.0, 0.0)
        base[19] = Vector3D(0.0, 0.0, 1.0)
        base[20] = Vector3D(0.0, -1.0, 0.0)

        base[21] = Vector3D(0.0, 0.0, 1.0)
        base[22] = Vector3D(-1.0, 0.0, 0.0)
        base[23] = Vector3D(0.0, -1.0, 0.0)

        result: List[Vector3D] = []

        for i in range(0, 24, 3):
            GeodesicSphere.interpolate(
                base[i],
                base[i + 1],
                base[i + 2],
                result,
                detail_level
            )

        return result