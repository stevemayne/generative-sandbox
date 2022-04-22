import colorsys
import random
import numpy as np
from shapes.wheels import Wheel
import pygame
import time

random.seed()

objects = []
size = [1000, 1000]
factor = 1
draw_wheels = True
BACKGROUND_COLOR = (0,0,0)

invalid = True
while invalid:
    invalid = False
    big_wheel_rotation_step = np.pi/2000 #0.0014
    big_wheel_radius_1 = 400
    big_wheel_radius_2 = big_wheel_radius_1 #random.randint(big_wheel_radius_1 - 20, big_wheel_radius_1 + 20) #370
    small_wheel_1_rotation_step = np.pi/random.randint(10, 40) #0.2064
    small_wheel_2_rotation_step = small_wheel_1_rotation_step * random.random() * 2 #np.pi/15 #0.2
    wheel_2_offset_from_wheel_1 = np.pi/random.randint(4, 8)
    wheel_1_size = random.randint(20, 200) #30
    wheel_2_size = random.randint(20, 200) #38
    arm_length_1 = random.randint(200, 350) #350
    arm_joint_1 = random.randint(100, 200)
    arm_length_2 = arm_joint_1 + random.randint(20, 100)
    hue = random.random()
    hue_step = 0.00005

    # Size checks
    distance_between_wheels = wheel_2_offset_from_wheel_1 * min(big_wheel_radius_2, big_wheel_radius_1)
    if arm_joint_1 + arm_length_2 <= (wheel_1_size + wheel_2_size + distance_between_wheels):
        invalid = True

bigger_wheel = None
big_wheel1 = Wheel(500, 500, big_wheel_rotation_step * factor, big_wheel_radius_1, 0) 
big_wheel2 = Wheel(500, 500, big_wheel_rotation_step * factor, big_wheel_radius_2, wheel_2_offset_from_wheel_1)
wheel1 = Wheel(0, 0, small_wheel_1_rotation_step * factor, wheel_1_size, 0, big_wheel1, color=(255,255,255)) 
wheel2 = Wheel(0, 0, small_wheel_2_rotation_step * factor, wheel_2_size, 0, big_wheel2, color=(255,255,255))

objects.clear()
objects.append(big_wheel1)
objects.append(big_wheel2)
objects.append(wheel1)
objects.append(wheel2)

frame_duration = 0.001
last_frame = time.time()
screen = pygame.display.set_mode(size)
draw_surface = pygame.Surface(size)
draw_surface.fill(BACKGROUND_COLOR)

last_pen_x = None
last_pen_y = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                draw_wheels = not draw_wheels
            elif event.key == pygame.K_RETURN:
                #reset()
                pass

    try:
        x, y = wheel1.position()
        x2, y2 = wheel2.position()

        distance_between_coords = np.sqrt(np.power(x2-x, 2) + np.power(y2-y, 2))

        # Work out the angle of the top of the triangle
        angle_from_1_to_2 = np.arctan2(x2-x, y2-y)

        # Use law of cosines to work out interior angle 
        gamma = np.arccos((np.power(distance_between_coords, 2) + \
            np.power(arm_length_2, 2) - \
            np.power(arm_joint_1, 2)) / 
            (2 * arm_length_2 * distance_between_coords))

        # Add them together
        arm_1_angle = angle_from_1_to_2 + gamma

        # Position of joint
        joint_x = x + np.sin(arm_1_angle) * arm_joint_1
        joint_y = y + np.cos(arm_1_angle) * arm_joint_1

        # Position of pen
        pen_x = x + np.sin(arm_1_angle) * arm_length_1
        pen_y = y + np.cos(arm_1_angle) * arm_length_1

        if last_pen_x is not None:
            rgb = colorsys.hsv_to_rgb(hue, 1, 1)
            r = round(rgb[0] * 255)
            g = round(rgb[1] * 255)
            b = round(rgb[2] * 255)
            rgb_ints = (r, g, b)
            pygame.draw.aaline(draw_surface, rgb_ints, (last_pen_x, last_pen_y), (pen_x, pen_y))
            hue += hue_step
            hue %= 1.0 # cap hue at 1.0

        last_pen_x = pen_x
        last_pen_y = pen_y

        #screen.fill((255, 255, 255))
        screen.blit(draw_surface, (0,0))

        if draw_wheels:
            pygame.draw.line(screen, (200, 200, 200), (joint_x, joint_y), (pen_x, pen_y))
            pygame.draw.line(screen, (200, 200, 200), (x, y), (joint_x, joint_y))
            pygame.draw.line(screen, (200, 200, 200), (x2, y2), (joint_x, joint_y))
            for object in objects:
                object.draw(screen)
        
        duration = time.time() - last_frame
        if duration < frame_duration:
            time.sleep(frame_duration - duration)
        
        # Flip the display
        pygame.display.flip()
        last_frame = time.time()

        for obj in objects:
            obj.step()
    except Exception as e:
        print(e)
        running = False

pygame.quit()