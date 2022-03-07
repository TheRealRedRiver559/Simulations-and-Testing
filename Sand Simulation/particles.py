class Particles:
    particle_instances = []
    particle_colors = {}
    def __init__(self, particle_id, particle_name, phase_type, physic_type, colors):
        self.__class__.particle_instances.append(self)
        self.__class__.particle_colors[particle_id] = colors
        self.name = particle_name
        self.particle_id = particle_id
        self.phase_type = phase_type
        self.physic_type = physic_type
        self.colors = colors

class initialize_particles:
    blank = Particles(0, 'blank', 'erase', 'erase', (0, 0, 0))
    sand = Particles(1, 'sand', 'solid', 'movableSolid', ((255, 255, 0)))
    water = Particles(2, 'water', 'liquid', 'liquid', (72, 209, 204))
    wall = Particles(3, 'wall', 'solid', 'nonmovableSolid', (160, 160, 160))
