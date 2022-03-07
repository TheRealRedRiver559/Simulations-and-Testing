import pygame
from settings import Settings
from particles import initialize_particles
from grid import Grid

settings = Settings()
screen = pygame.display.set_mode(settings.SIZE)


settings.window = screen
particles = initialize_particles()
grid = Grid(settings, particles)
grid.current_particle = particles.sand
 
fps_clock = pygame.time.Clock()

running = True
paused = False
dragging = False

while running:
    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = round(mouse_x//settings.CELL_SIZE), round(mouse_y//settings.CELL_SIZE)
            grid.mouse_draw(grid_x, grid_y)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                grid.current_particle = particles.sand
            elif event.key == pygame.K_2:
                grid.current_particle = particles.water
            elif event.key == pygame.K_3:
                grid.current_particle = particles.wall
            elif event.key == pygame.K_4:
                grid.current_particle = particles.blank
            elif event.key == pygame.K_q:
                grid.resetGrid()
            elif event.key == pygame.K_SPACE:
                paused = not paused
            
    if paused == False:
        grid.simulateParticles()
    grid.draw_particles()
    fps_clock.tick(Settings.MAX_FPS)
    pygame.display.update()
    pygame.display.set_caption("Falling Sand - FPS: {}".format(int(fps_clock.get_fps())))

    pygame.display.flip()

pygame.quit()
