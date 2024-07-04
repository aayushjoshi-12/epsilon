import pygame
from vectors import Vector, Force
from objects import Surface, Rectangle, Circle
from utils import display, debug, update, check_collision
from constants import screen_width, screen_height, dt, fps

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("My Pygame Window")

rectangle1 = Rectangle(Vector(100, 100), 10, 100, 100, color=(0, 0, 255))
rectangle2 = Rectangle(Vector(600, 100), 10, 100, 100, color=(0, 255, 0))

circle1 = Circle(Vector(100, 100), 1, 50, color=(0, 0, 255))
circle2 = Circle(Vector(500, 100), 1, 50, color=(0, 255, 0))

right_force = Force(10, 0, rectangle1.position, False)
left_force = Force(-10, 0, rectangle2.position, False)

earth = Surface(Vector(screen_width / 2, screen_height - 25))

upward_force1 = Force(0, -100, rectangle1.position)
upward_force2 = Force(0, -100, rectangle2.position)

circle1.apply_force(upward_force1)
circle2.apply_force(upward_force2)
circle1.velocity = Vector(100, 0)
circle2.velocity = Vector(-100, 0)

# rectangle1.apply_force(upward_force1)
# rectangle2.apply_force(upward_force2)
rectangle1.velocity = Vector(100, 0)
rectangle2.velocity = Vector(-100, 0)

objects = [earth, rectangle1, rectangle2]

running = True
engine_running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                engine_running = not engine_running

    screen.fill((0, 0, 0))
    clock.tick(fps)
    display(objects)
    debug([rectangle1, rectangle2])
    if engine_running:
        update(objects, dt)
        check_collision(objects)

    pygame.display.flip()

pygame.quit()
