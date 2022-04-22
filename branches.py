import random
import numpy as np
import pygame
import time
from shapes.branch import Branch

size = (1000,1000)
BACKGROUND_COLOR = (0,0,0)
BRANCH_STEP = 2

screen = pygame.display.set_mode(size)
draw_surface = pygame.Surface(size)
draw_surface.fill(BACKGROUND_COLOR)

branches = [] #type: list(Branch)

def perp_left(angle):
    result = angle - (np.pi/2)
    if result < 0:
        result += np.pi * 2
    return result

def perp_right(angle):
    result = angle + (np.pi/2)
    if result > np.pi * 2:
        result -= np.pi * 2
    return result

def reset():
    global curvature, branches, branch_probability, branch_left_probability
    draw_surface.fill(BACKGROUND_COLOR)
    branches.clear()
    curvature = random.randrange(0, 20) / 1000
    branch_probability = 1.0 - (random.random() / 20.0)
    branch_left_probability = random.random()
    for _ in range(0,3):
        start_angle = random.random() * np.pi * 2
        branches.append(Branch(500, 500, start_angle, curvature, BRANCH_STEP))

reset()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                reset()

    all_dead = True
    for branch in branches:
        if branch.dead:
            continue
        all_dead = False
        origin = (branch.x, branch.y)
        branch.step()
        if random.random() > branch_probability:
            if random.random() >= branch_left_probability:
                new_angle = perp_left(branch.direction)
                new_rotation = branch.rotation
            else:
                new_angle = perp_right(branch.direction)
                new_rotation = -branch.rotation
            branches.append(Branch(branch.x, branch.y, new_angle, new_rotation, branch.speed))
        destination = (int(branch.x), int(branch.y))
        if destination[0] >= size[0] or destination[1] >= size[1] or destination[0] < 0 or destination[1] < 0:
            branch.dead = True
        else:
            pixel = draw_surface.get_at(destination)
            if pixel != (BACKGROUND_COLOR):
                #This branch has run its course
                branch.dead = True
        pygame.draw.aaline(draw_surface, branch.color, origin, destination)
    
    screen.blit(draw_surface, (0,0))
    pygame.display.flip()

    if all_dead:
        time.sleep(5)
        reset()
