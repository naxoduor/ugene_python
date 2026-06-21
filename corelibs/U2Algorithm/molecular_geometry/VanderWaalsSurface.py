FACTOR = 64


class VanDerWaalsSurface:
    def __init__(self):
        self.faces = []

    def calculate(self, atoms):
        # Van der Waals surface calculation
        overall = len(atoms)
        counter = 0

        detail_level = 2
        if len(atoms) > 10000:
            detail_level = 1

        for a in atoms:
            neighbors = self.find_atom_neighbors(a, atoms)
            surface = self.get_atom_surface_dots(a, detail_level)

            surface_dots = surface.get_vertices()
            reduced_vertices = []

            for v in surface_dots:
                if self.vertex_neighbors_one_of(v, neighbors):
                    continue
                reduced_vertices.append(v)

            surface_faces = surface.get_faces()

            for face in surface_faces:
                if (face.v[0] in reduced_vertices or
                    face.v[1] in reduced_vertices or
                    face.v[2] in reduced_vertices):
                    self.faces.append(face)

            counter += 1
            progress = counter * 100 // overall

        return self.faces, progress

    # ---- placeholders for external dependencies ----
    def find_atom_neighbors(self, atom, atoms):
        raise NotImplementedError

    def get_atom_surface_dots(self, atom, detail_level):
        raise NotImplementedError

    def vertex_neighbors_one_of(self, v, neighbors):
        raise NotImplementedError

    # ---- memory estimate ----
    @staticmethod
    def estimate_memory_usage(number_of_atoms: int) -> int:
        return int(number_of_atoms * FACTOR * 8 * 3 * 6 * 1.5)


class VanDerWaalsSurfaceFactory:
    def create_instance(self):
        return VanDerWaalsSurface()