import random
from xml.dom import INDEX_SIZE_ERR
import pygame
from particles import Particles

#main class used for pretty much everything
class Grid:
    def __init__(self, settings, particles):
        self.particle_list = Particles.particle_instances
        self.current_particle = None
        self.current_color = None
        self.reset = False
        self.cursor_draw = True #Test to increase cursor size
        self.particles = particles
        self.rows = settings.rows
        self.columns = settings.columns
        self.window = settings.window
        self.cell_size = settings.CELL_SIZE 
        #this makes the "future" and "current" grid according to size
        self.current_grid = [[5 if (y==0 or self.columns-y-1 == 0) or (x==0 or self.rows-x-1 == 0) else 0 for x in range(self.rows)] for y in range(self.columns)]
        self.future_grid = [[5 if (y==0 or self.columns-y-1 == 0) or (x==0 or self.rows-x-1 == 0) else 0 for x in range(self.rows)] for y in range(self.columns)]

    def resetGrid(self):
        #resets both grids, for clearing particles
        self.reset = True
        self.current_grid = [[5 if (y==0 or self.columns-y-1 == 0) or (x==0 or self.rows-x-1 == 0) else 0 for x in range(self.rows)] for y in range(self.columns)]
        self.future_grid = [[5 if (y==0 or self.columns-y-1 == 0) or (x==0 or self.rows-x-1 == 0) else 0 for x in range(self.rows)] for y in range(self.columns)]
    
    #this goes through each row and each column spot on the grid checking and updating them according to their 'physic_type'
    def simulateParticles(self):
        for x in range(self.rows):
            for y in range(self.columns):
                for obj in self.particle_list:
                    if  self.current_grid[x][y] == obj.particle_id:
                        self.updateParticle(obj, x, y)

    def updateParticle(self, particle, x, y):
        match particle.physic_type:
            case 'movableSolid':
                self.update_movableSolid(particle, x, y)
            case 'liquid':
                self.update_liquids(particle, x, y)

    #water is very broken...
    def update_movableSolid(self, particle, x, y):
        if self.future_grid[x][y+1] == 0:
            self.future_grid[x][y] =  0
            self.future_grid[x][y+1] = particle.particle_id

        elif self.future_grid[x+1][y+1] == 0 and self.future_grid[x-1][y+1] == 0:
            self.future_grid[x][y] = 0
            choice = random.randint(0, 1)
            if choice == 0:
                self.future_grid[x+1][y+1] = particle.particle_id
            else:
                self.future_grid[x-1][y+1] = particle.particle_id

        elif self.future_grid[x+1][y+1] == 0:
            self.future_grid[x][y] = 0
            self.future_grid[x+1][y+1] = particle.particle_id

        elif self.future_grid[x-1][y+1] == 0:
            self.future_grid[x][y] = 0
            self.future_grid[x-1][y+1] = particle.particle_id

    def update_liquids(self, particle, x, y):
        if self.future_grid[x][y+1] == 0:
            self.future_grid[x][y] =  0
            self.future_grid[x][y+1] = particle.particle_id
        elif self.future_grid[x+1][y+1] == 0 and self.future_grid[x-1][y+1] == 0:

            self.future_grid[x][y] = 0
            choice = random.randint(0, 1)
            if choice == 0:
                self.future_grid[x+1][y+1] = particle.particle_id
            else:
                self.future_grid[x-1][y+1] = particle.particle_id
        elif self.future_grid[x+1][y+1] == 0:
            self.future_grid[x][y] = 0
            self.future_grid[x+1][y+1] = particle.particle_id

        elif self.future_grid[x-1][y+1] == 0:
            self.future_grid[x][y] = 0
            self.future_grid[x-1][y+1] = particle.particle_id

        elif self.future_grid[x-1][y] == 0 and self.future_grid[x+1][y] == 0:
            self.future_grid[x][y] = 0
            choice = random.randint(0, 1)
            if choice == 0:
                self.future_grid[x+1][y] = particle.particle_id
            else:
                self.future_grid[x-1][y] = particle.particle_id

        elif self.future_grid[x-1][y] == 0:
            self.future_grid[x][y] = 0
            self.future_grid[x-1][y] = particle.particle_id
        
        elif self.future_grid[x+1][y] == 0:
            self.future_grid[x][y] = 0
            self.future_grid[x+1][y] = particle.particle_id

    def draw_particles(self):
        for x in range(1, self.rows-1):
            for y in range(1, self.columns-1):
                if self.current_grid[x][y] == self.future_grid[x][y] and self.reset == False:
                    pass
                else:
                    self.current_grid[x][y] = self.future_grid[x][y]
                    pygame.draw.rect(self.window, (Particles.particle_colors[self.future_grid[x][y]]), [int(x * self.cell_size), int((y) * self.cell_size), self.cell_size, self.cell_size], 0)
        if self.reset == True:
            self.reset = False
        
    def mouse_draw(self, x, y):
        for particle in self.particle_list:
            if self.future_grid[x][y] != 0 and self.current_particle.particle_id != 0:

                return
            if self.cursor_draw:
                for width in range(5):
                    for height in range(5):
                        try:
                            self.future_grid[x-width][y+width] = (self.current_particle.particle_id)
                        except IndexError:
                            pass
            else:
                self.future_grid[x][y] = (self.current_particle.particle_id)

                
