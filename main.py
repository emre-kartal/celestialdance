#!/usr/bin/env python3

# the celestial dance v0.1
# a simple simulation of the solar system
# actually copilot created this name, i'm too lazy to think of a name

# i know this is a mess, but i'm too lazy to clean it up
# i'm also too lazy to make a proper readme
# i'm also too lazy to make a proper anything
# and i'm also too lazy to make a proper comment
# and believe or or not, i'm so lazy that these comment lines are written by copilot
# haha

# this code implements newton's law of universal gravitation but
# does not implement relativistic effects

# also, the code is not optimized at all
# i know i could put the planet data in a json file or something, haha this is so stupid
# fun fact: i'm not even a programmer, i'm a high school student
# i'm just doing this for fun
# i'm also too lazy to make a proper license
# so, do whatever you want with this code
# i'm too lazy to care

# this copilot thing is so cool, it completes my sentences
# if you could just implement the relativistic effects, that would be great
# i'm not sure if not implementing the relativistic effects makes such a big difference
# planets sometimes just fly out of orbit and i don't know if it is because of the lack of
# relativistic effects or if it is because of the lack of precision or if it just the orbital values are wrong
# also increasing the time multiplier makes the planets fly out of orbit
# if i can learn how to project a 3d space to a 2d space, i can make a 3d version of this
# but i think i'm gonna use c or c++ for that or write c code in python
# help me

# date: 2024-07-07
# author: me (emre kartal)
# sources: i don't know, i just wrote this code from scratch
# i don't know if this code is similar to any other code
# i'm too lazy to check

import pygame
import pygame.gfxdraw
import math
import time
import decimal # for high precision floating point numbers. yeah. really. i'm not kidding.

# pip install pygame / pip3 install pygame
# or if you are a gigachad arch user and think pip sucks, pacman -S python-pygame
# and it should work with
# python3 main.py
# or
# python main.py
# or download universe sandbox 2 and play that instead

decimal.getcontext().prec = 100 # floating point precision. i don't know it makes a difference or the value is too high or too low.

# screen size
W_WIDTH = 1350
W_HEIGHT = 900


window = pygame.display.set_mode((W_WIDTH, W_HEIGHT))

pygame.font.init()

pygame.display.set_caption("Celestial Dance") # oh god. how cool of a name is that?

font = pygame.font.Font(None, 32)

map_size = (decimal.Decimal(200000), decimal.Decimal(200000)) #in AU

PIXEL_SIZE = decimal.Decimal(0.000009) #in AU
LEFT_TOP_POS = (decimal.Decimal(map_size[0]/ 2) - (decimal.Decimal(W_WIDTH) * decimal.Decimal(PIXEL_SIZE) / decimal.Decimal(2)), decimal.Decimal(map_size[0] / 2) - (decimal.Decimal(W_HEIGHT) * decimal.Decimal(PIXEL_SIZE) / decimal.Decimal(2))) #in AU
AU = decimal.Decimal(149597871) #in kms
SOLAR_MASS = decimal.Decimal(1.9891) * decimal.Decimal(10) ** decimal.Decimal(30) #kgs
G_CONST = decimal.Decimal(6.67428) * decimal.Decimal(10) ** decimal.Decimal(-11) # who the heck cares about the units
TIME_MULTIPLIER = decimal.Decimal(10800) #in seconds
TRACEPOINT_COUNT = decimal.Decimal(round(0 * (1 / math.log(TIME_MULTIPLIER + 1, 10))))
# the tracepoint count determines how many tracepoints are drawn. it is calculated by the formula above.

planet_size_scalar = decimal.Decimal(1) 
# if planets are hard to see, change

running = True

tracepoints = []

camera_locked = True 

# i didn't add the code for locking the camera to the object you want to lock. change the value
# below to lock the camera to the object you want to lock. the value is the index of the object in the system list.

cam_object = 3


# i know adding every value in au is stupid but i'm too lazy to change it, it was an ititial idea and a bad one
# and somewhere in this code, there is a variable named diameters_in_pixels.
# you guessed it, values are radiuses in pixels. isn't that hilariously stupid?

# god help me at this point
# i forgot to take my meds
# who is the guy standing behind me

sizes = { 
    "sun": decimal.Decimal(696340) / decimal.Decimal(AU),
    "mercury": decimal.Decimal(2440) / decimal.Decimal(AU),
    "venus": decimal.Decimal(6051) / decimal.Decimal(AU),
    "earth": decimal.Decimal(6378) / decimal.Decimal(AU),
    "moon": decimal.Decimal(1740) / decimal.Decimal(AU),
    "mars": decimal.Decimal(3389) / decimal.Decimal(AU),
    "phobos": decimal.Decimal(12) / decimal.Decimal(AU),
    "deimos": decimal.Decimal(6.25) / decimal.Decimal(AU),
    "jupiter": decimal.Decimal(69911) / decimal.Decimal(AU),
    "io": decimal.Decimal(1821) / decimal.Decimal(AU),
    "europa": decimal.Decimal(1560) / decimal.Decimal(AU),
    "ganymede": decimal.Decimal(2634) / decimal.Decimal(AU),
    "callisto": decimal.Decimal(2410) / decimal.Decimal(AU),
    "saturn": decimal.Decimal(58232) / decimal.Decimal(AU),
    "titan": decimal.Decimal(2576) / decimal.Decimal(AU),
    "uranus": decimal.Decimal(25362) / decimal.Decimal(AU),
    "neptune": decimal.Decimal(24622) / decimal.Decimal(AU),
    "pluto": decimal.Decimal(1188) / decimal.Decimal(AU),
    "big": decimal.Decimal(1392000) / decimal.Decimal(AU)
}

# if the stupidity of the code is not enough, here is the mass of the objects in solar masses
# you have to calculate the mass of the objects in solar masses!!! stupid i know

masses = {
    "sun": decimal.Decimal(1),
    "mercury": decimal.Decimal(3.285) * decimal.Decimal(10) ** decimal.Decimal(-7),
    "venus": decimal.Decimal(4.867) * decimal.Decimal(10) ** decimal.Decimal(-6),
    "earth": decimal.Decimal(5.972) * decimal.Decimal(10) ** decimal.Decimal(-6),
    "moon": decimal.Decimal(3.69363029) * decimal.Decimal(10) ** decimal.Decimal(-8),
    "phobos": decimal.Decimal(5.3290) * decimal.Decimal(10) ** decimal.Decimal(-15),
    "deimos": decimal.Decimal(7.5913) * decimal.Decimal(10) ** decimal.Decimal(-16),
    "mars": decimal.Decimal(6.39) * decimal.Decimal(10) ** decimal.Decimal(-7),
    "jupiter": decimal.Decimal(1.898) * decimal.Decimal(10) ** decimal.Decimal(-3),
    "io": decimal.Decimal(4.4904228) * decimal.Decimal(10) ** decimal.Decimal(-8),
    "europa": (decimal.Decimal(4.799844) * decimal.Decimal(10) ** decimal.Decimal(22)) / decimal.Decimal(SOLAR_MASS),
    "ganymede": (decimal.Decimal(1.4819) * decimal.Decimal(10) ** decimal.Decimal(23)) / decimal.Decimal(SOLAR_MASS),
    "callisto": (decimal.Decimal(1.075938) * decimal.Decimal(10) ** decimal.Decimal(23)) / decimal.Decimal(SOLAR_MASS),
    "saturn": decimal.Decimal(5.683) * decimal.Decimal(10) ** decimal.Decimal(-4),
    "titan": (decimal.Decimal(1.3452) * decimal.Decimal(10) ** decimal.Decimal(23)) / decimal.Decimal(SOLAR_MASS),
    "uranus": decimal.Decimal(8.681) * decimal.Decimal(10) ** decimal.Decimal(-5),
    "neptune": decimal.Decimal(1.024) * decimal.Decimal(10) ** decimal.Decimal(-4),
    "pluto": (decimal.Decimal(1.303) * decimal.Decimal(10) ** decimal.Decimal(22)) / decimal.Decimal(SOLAR_MASS),
}

# you guessed it, the distances from the sun in au

distances_from_sun = {
    "mercury": decimal.Decimal(0.39),
    "venus": decimal.Decimal(0.72),
    "earth": decimal.Decimal(1),
    "moon": decimal.Decimal(1 + 0.00256955529),
    "mars": decimal.Decimal(1.52),
    "phobos": decimal.Decimal(1.52 + 0.00004010752) + decimal.Decimal(6794) / decimal.Decimal(AU),
    "deimos": decimal.Decimal(1.52 + 0.00015680704) + decimal.Decimal(3389) / decimal.Decimal(AU),
    "jupiter": decimal.Decimal(5.2),
    "io": decimal.Decimal(5.2) + (decimal.Decimal(421700) / decimal.Decimal(AU)),
    "europa": decimal.Decimal(5.2) + (decimal.Decimal(671034) / decimal.Decimal(AU)),
    "ganymede": decimal.Decimal(5.2) + (decimal.Decimal(1070412) / decimal.Decimal(AU)),
    "callisto": decimal.Decimal(5.2) + (decimal.Decimal(1882709) / decimal.Decimal(AU)),
    "saturn": decimal.Decimal(9.58),
    "titan": decimal.Decimal(9.58) + (decimal.Decimal(1221870) / decimal.Decimal(AU)),
    "enceladus": decimal.Decimal(9.58) + (decimal.Decimal(238000) / decimal.Decimal(AU)),
    "uranus": decimal.Decimal(19.22),
    "neptune": decimal.Decimal(30.05),
    "pluto": decimal.Decimal(5.906 * 10 ** 9) / decimal.Decimal(AU)

}

# maybe this is the only thing that makes sense in this code
# the colors of the planets
# yeah, rgb. and i know sun is not a planet

planet_colors = {
    "sun": (255, 255, 0),
    "mercury": (200, 200, 200),
    "venus": (255, 200, 0),
    "earth": (0, 67, 255),
    "moon": (200, 200, 200),
    "mars": (255, 0, 0),
    "phobos": (169, 169, 169),
    "deimos": (105, 105, 105),
    "jupiter": (255, 200, 0),
    "io": (255, 223, 0),
    "europa": (255, 250, 250),
    "ganymede": (211, 211, 211),
    "callisto": (169, 169, 169), 
    "saturn": (255, 200, 0),
    "titan": (210, 180, 140),
    "enceladus": (240, 240, 240),
    "uranus": (0, 255, 255),
    "neptune": (0, 0, 255),
    "pluto": (210, 180, 140)

}

# the orbital velocities of the planets in m/s. some
# values in this code is in au, some in kms, some in meters
# and some in solar masses

orbital_velocities = {
    "mercury": decimal.Decimal(47360),
    "venus": decimal.Decimal(35020),
    "earth": decimal.Decimal(29784),
    "moon": decimal.Decimal(1022 + 29784),
    "mars": decimal.Decimal(24077),
    "phobos": decimal.Decimal(2138 + 24077),
    "deimos": decimal.Decimal(1351 + 24077),
    "jupiter": decimal.Decimal(13070),
    "io": decimal.Decimal(17340 + 13070),
    "europa": decimal.Decimal(13740 + 13070),
    "ganymede": decimal.Decimal(10880 + 13070),
    "callisto": decimal.Decimal(8200 + 13070), 
    "saturn": decimal.Decimal(9644),
    "titan": decimal.Decimal(5570 + 9644),
    "uranus": decimal.Decimal(6810),
    "neptune": decimal.Decimal(5430),
    "pluto": decimal.Decimal(4748)

}

center_x = decimal.Decimal(100000)
center_y = decimal.Decimal(100000)
# these two are the center of the solar system. you know, size was specified above. 200000 au.

# adding objects is frickin boring
# pos in au, mass in solar masses, diameter in au, velocity vector in m/s, color
# god help you if you want to add a new object at this point

system = [
    [(center_x, center_y), masses["sun"], sizes["sun"], (0, 0), planet_colors["sun"]],
    [(center_x + distances_from_sun["mercury"], center_y), masses["mercury"], sizes["mercury"], (0, orbital_velocities["mercury"]), planet_colors["mercury"]],
    [(center_x + distances_from_sun["venus"], center_y), masses["venus"], sizes["venus"], (0, orbital_velocities["venus"]), planet_colors["venus"]],
    [(center_x + distances_from_sun["earth"], center_y), masses["earth"], sizes["earth"], (0, orbital_velocities["earth"]), planet_colors["earth"]],
    [(center_x + distances_from_sun["moon"], center_y), masses["moon"], sizes["moon"], (0, orbital_velocities["moon"]), planet_colors["moon"]],
    [(center_x + distances_from_sun["mars"], center_y), masses["mars"], sizes["mars"], (0, orbital_velocities["mars"]), planet_colors["mars"]],
    [(center_x + distances_from_sun["phobos"], center_y), masses["phobos"], sizes["phobos"], (0, orbital_velocities["phobos"]), planet_colors["phobos"]],
    [(center_x + distances_from_sun["deimos"], center_y), masses["deimos"], sizes["deimos"], (0, orbital_velocities["deimos"]), planet_colors["deimos"]],
    [(center_x + distances_from_sun["jupiter"], center_y), masses["jupiter"], sizes["jupiter"], (0, orbital_velocities["jupiter"]), planet_colors["jupiter"]],
    [(center_x + distances_from_sun["io"], center_y), masses["io"], sizes["io"], (0, orbital_velocities["io"]), planet_colors["io"]],
    [(center_x + distances_from_sun["europa"], center_y), masses["europa"], sizes["europa"], (0, orbital_velocities["europa"]), planet_colors["europa"]],
    [(center_x + distances_from_sun["ganymede"], center_y), masses["ganymede"], sizes["ganymede"], (0, orbital_velocities["ganymede"]), planet_colors["ganymede"]],
    [(center_x + distances_from_sun["callisto"], center_y), masses["callisto"], sizes["callisto"], (0, orbital_velocities["callisto"]), planet_colors["callisto"]],
    [(center_x + distances_from_sun["saturn"], center_y), masses["saturn"], sizes["saturn"], (0, orbital_velocities["saturn"]), planet_colors["saturn"]],
    [(center_x + distances_from_sun["titan"], center_y), masses["titan"], sizes["titan"], (0, orbital_velocities["titan"]), planet_colors["titan"]],    [(center_x + distances_from_sun["uranus"], center_y), masses["uranus"], sizes["uranus"], (0, orbital_velocities["uranus"]), planet_colors["uranus"]],
    [(center_x + distances_from_sun["neptune"], center_y), masses["neptune"], sizes["neptune"], (0, orbital_velocities["neptune"]), planet_colors["neptune"]],
    [(center_x + distances_from_sun["pluto"], center_y), masses["pluto"], sizes["pluto"], (0, orbital_velocities["pluto"]), planet_colors["pluto"]]
    ]

# does python come with a built-in vector class? i don't know
# i'm too lazy to check
# does numpy have something like this?


# the 10 or something functions below are the most important functions in this code. 
# they calculate the forces, accelerations, velocities and positions of the planets.
# isn't that cool?

def calculate_force_vectors(object1, object2):
    mass_sm1 = object1[1]
    mass_sm2 = object2[1]
    mass_kg1 = mass_sm1 * SOLAR_MASS
    mass_kg2 = mass_sm2 * SOLAR_MASS
    pos1 = object1[0]
    pos2 = object2[0]
    distance_au =((pos1[0] - pos2[0]) ** decimal.Decimal(2) + (pos1[1] - pos2[1]) ** decimal.Decimal(2)).sqrt()
    distance_meters = decimal.Decimal(distance_au) * decimal.Decimal(AU) * decimal.Decimal(1000)
    force_scalar = (G_CONST * mass_kg1 * mass_kg2) / ((distance_meters) ** 2)
    object1to2_vec = (pos2[0] - pos1[0]) / distance_au, (pos2[1] - pos1[1]) / distance_au
    object2to1_vec = -object1to2_vec[0], -object1to2_vec[1]
    return object1to2_vec, object2to1_vec, force_scalar

# the function above calculates the force vectors between two objects. returns the opposite vectors and the scalar of the vectors

def calculate_all_force_vectors_on_object(index):
    object = system[index]
    result_vec = (0, 0)
    for i in range(len(system)):
        if i == index:
            continue
        vec, _, scalar = calculate_force_vectors(object, system[i])
        result_vec = add_vectors(result_vec, scale_vector(vec, scalar))
    return result_vec

# aaaand this function calculates the sum of all force vectors on an object. it does this by calling the function above for every two objects.
# what was that? combination? permutation? it chooses every two objects and calculates the force vectors between them.

def calculate_accel_vector(vec, mass):
    return scale_vector(vec, 1 / mass)

#the above is the easiest to understand. it calculates the acceleration vector by dividing the force vector by the mass of the object.

def calc_object_final_pos(index, deltatime):
    sum_of_forces = calculate_all_force_vectors_on_object(index)
    accel_vec = calculate_accel_vector(sum_of_forces, system[index][1] * SOLAR_MASS)
    velocity_vec = scale_vector(system[index][3], decimal.Decimal(1))
    delta_x = add_vectors(scale_vector(velocity_vec, deltatime), scale_vector(accel_vec, (decimal.Decimal(1) / decimal.Decimal(2)) * (decimal.Decimal(deltatime) ** decimal.Decimal(2))))
    return add_vectors(scale_vector(delta_x, decimal.Decimal(1) / (decimal.Decimal(AU) * decimal.Decimal(1000))), system[index][0])

# the function above calculates the final position of an object by using the acceleration vector and the velocity vector.
# if you look carefully it takes deltatime as an argument. it is the time passed since the last frame.

def calc_object_final_vel(index, deltatime):
    sum_of_forces = calculate_all_force_vectors_on_object(index)
    accel_vec = calculate_accel_vector(sum_of_forces, system[index][1] * SOLAR_MASS)
    velocity_vec = system[index][3]
    final_v = add_vectors(velocity_vec, scale_vector(accel_vec, deltatime))
    return final_v

# the function above calculates the final velocity of an object by using the acceleration vector.
# again, it takes deltatime as an argument. it is the time passed since the last frame.

def calculate_all_final_poses_and_vels(deltatime):
    final_poses = []
    final_vels = []
    for i in range(len(system)):
        final_poses.append(calc_object_final_pos(i, deltatime))
        final_vels.append(calc_object_final_vel(i, deltatime))
    return final_poses, final_vels

# the function above calculates the final positions and velocities of all objects in the system. 
# it does this by calling the functions above for every object in the system.
# it returns the values but does not apply them to the system.

def apply_final_poses_and_vels(poses, vels):
    ctr = 0
    for pos in poses:
        system[ctr][0] = pos
        ctr += 1
    ctr = 0
    for vel in vels:
        system[ctr][3] = vel
        ctr += 1

# this applies the values calculated by the function above to the system.

# and the functions below are just vector operations. they are boring. are you still reading this? why?
        
def add_vectors(vec1, vec2):
    return vec1[0] + vec2[0], vec1[1] + vec2[1]
def scale_vector(vec, scalar):
    return vec[0] * scalar, vec[1] * scalar
def sub_vectors(vec1, vec2):
    return vec1[0] - vec2[0], vec1[1] - vec2[1]

clock = pygame.time.Clock() # to limit the fps.
dt = clock.tick(60) # to get the time passed since the last frame. takes limit fps as an argument.
dt = decimal.Decimal(dt / 1000) # dt is actually in milliseconds. i learned this the hard way.
ctr = 0

# why the heck did i add this timestamp thing? i don't remember.

timestamps = []
for object in system:
    timestamps.append(0)

# i actually forgot what i added timestamps for

pressed_buttons = {}
pressed_buttons[pygame.K_z] = False
pressed_buttons[pygame.K_x] = False
pressed_buttons[pygame.K_LEFT] = False
pressed_buttons[pygame.K_RIGHT] = False
pressed_buttons[pygame.K_DOWN] = False
pressed_buttons[pygame.K_UP] = False

# creating a dict entry for every key in the pressed_buttons dict, there must be a better way to do this
# like, really a better way.

offset_x = decimal.Decimal(0)
offset_y = decimal.Decimal(0)
#these two are for camera movement

anti_repeat_buttons = {}
while running:

    window.fill((0, 0, 0))
    start = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pressed_buttons[event.key] = True
        if event.type == pygame.KEYUP:
            pressed_buttons[event.key] = False

    if pressed_buttons[pygame.K_z]:
        if not anti_repeat_buttons[pygame.K_z]:
            anti_repeat_buttons[pygame.K_z] = True
            PIXEL_SIZE = PIXEL_SIZE / decimal.Decimal(1.44)
    else:
        anti_repeat_buttons[pygame.K_z] = False
    if pressed_buttons[pygame.K_x]:
        if not anti_repeat_buttons[pygame.K_x]:
            anti_repeat_buttons[pygame.K_x] = True
            PIXEL_SIZE = PIXEL_SIZE * decimal.Decimal(1.44)
    else:
        anti_repeat_buttons[pygame.K_x] = False
    if pressed_buttons[pygame.K_LEFT]:
        if not anti_repeat_buttons[pygame.K_LEFT]:
            anti_repeat_buttons[pygame.K_LEFT] = True
            offset_x -= (decimal.Decimal(PIXEL_SIZE) * decimal.Decimal(W_WIDTH)) / decimal.Decimal(20)
            camera_locked = False
    else:
        anti_repeat_buttons[pygame.K_LEFT] = False
    if pressed_buttons[pygame.K_RIGHT]:
        if not anti_repeat_buttons[pygame.K_RIGHT]:
            anti_repeat_buttons[pygame.K_RIGHT] = True
            offset_x += (decimal.Decimal(PIXEL_SIZE) * decimal.Decimal(W_WIDTH)) / decimal.Decimal(20)
            camera_locked = False
    else:
        anti_repeat_buttons[pygame.K_RIGHT] = False
    if pressed_buttons[pygame.K_DOWN]:
        if not anti_repeat_buttons[pygame.K_DOWN]:
            anti_repeat_buttons[pygame.K_DOWN] = True
            offset_y += (decimal.Decimal(PIXEL_SIZE) * decimal.Decimal(W_WIDTH)) / decimal.Decimal(20)
            camera_locked = False

    else:
        anti_repeat_buttons[pygame.K_DOWN] = False
    if pressed_buttons[pygame.K_UP]:
        if not anti_repeat_buttons[pygame.K_UP]:
            anti_repeat_buttons[pygame.K_UP] = True
            offset_y -= (decimal.Decimal(PIXEL_SIZE) * decimal.Decimal(W_WIDTH)) / decimal.Decimal(20)
            camera_locked = False

    else:
        anti_repeat_buttons[pygame.K_UP] = False # why the fcuk did i add the up key and not the others? the code works but why?


    if camera_locked:
        offset_x = system[cam_object][0][0] - decimal.Decimal(100000)
        offset_y = system[cam_object][0][1] - decimal.Decimal(100000)
        # these two lock the camera to the chosen object
    
    LEFT_TOP_POS = (decimal.Decimal(100000) - (decimal.Decimal(W_WIDTH) * decimal.Decimal(PIXEL_SIZE) / decimal.Decimal(2)) + offset_x, decimal.Decimal(100000) - (decimal.Decimal(W_HEIGHT) * decimal.Decimal(PIXEL_SIZE) / decimal.Decimal(2)) + offset_y)
    # this is the top left position of the camera. can you believe it?
    
    #print(offset_x, offset_y)
    #print(LEFT_TOP_POS)
    

    # camera draw
    right_bottom = (PIXEL_SIZE * W_WIDTH, PIXEL_SIZE * W_HEIGHT)
    object_ctr = 0
    for object in system:
        pos_x = object[0][0] - LEFT_TOP_POS[0]
        pos_y = object[0][1] - LEFT_TOP_POS[1]
        mass = object[1]
        diameter = object[2]
        velocity = object[3]
        color = object[4]

        # fuck this is a mess

        pos_in_pixels = (round(pos_x / PIXEL_SIZE), round(pos_y / PIXEL_SIZE))
        diameter_in_pixels = round((diameter * planet_size_scalar) / PIXEL_SIZE)
    
        # kilometers? meters? au? pixels? solar masses? kilograms? why did i made such a mess?

        for point in tracepoints:
            trace_pos_in_pixels = (round((point[0][0] - LEFT_TOP_POS[0]) / PIXEL_SIZE), round((point[0][1] - LEFT_TOP_POS[1]) / PIXEL_SIZE))
            if not (trace_pos_in_pixels[0] > W_WIDTH or trace_pos_in_pixels[0] < 0) and not (trace_pos_in_pixels[1] > W_HEIGHT or trace_pos_in_pixels[1] < 0):
                pygame.gfxdraw.pixel(window, trace_pos_in_pixels[0], trace_pos_in_pixels[1], point[1])

        # this is the tracepoints. they are the points that the planets have passed. they are drawn as pixels.
        # this thing makes the simulation look cool. i think. and makes planets more visible.
        
        
        if not (pos_in_pixels[0] > W_WIDTH + diameter_in_pixels or pos_in_pixels[0] < 0 - diameter_in_pixels) and not (pos_in_pixels[1] > W_HEIGHT + diameter_in_pixels or pos_in_pixels[1] < 0 - diameter_in_pixels):
            if diameter_in_pixels < (W_WIDTH * 2) and diameter_in_pixels < (W_HEIGHT * 2):
                pygame.gfxdraw.aacircle(window, pos_in_pixels[0], pos_in_pixels[1], diameter_in_pixels, color)

        # this draws the planets. it is an anti-aliased circle. it is cool. i think. it is also slow. i think.
        # i could use pygame.draw.circle but it is not anti-aliased.
        # im gonna go play some undertale now.

        
        if start - timestamps[object_ctr] > (decimal.Decimal(0.2) / TIME_MULTIPLIER):
            tracepoints.append(((pos_x + LEFT_TOP_POS[0], pos_y + LEFT_TOP_POS[1]), color))
            timestamps[object_ctr] = start
        #creates the tracepoints.


        if len(tracepoints) > TRACEPOINT_COUNT:
            tracepoints.pop(0)
        # cleans the old tracepoints.
        
        object_ctr += 1

    # this whole camera draw thing is a mess. i wouldn't touch it if i were you. it works. that's enough for me.
    # i don't think anyone will ever read this code. i'm just writing this for fun. i'm not even a programmer.
    # but i pity the person who will read this code.

    pygame.draw.line(window, (255, 255, 255), (20, W_HEIGHT - 20), (W_WIDTH - 20, W_HEIGHT - 20))  
    # this is the line at the bottom of the screen. it provides a distance scale reference

    text = font.render("{} AU, {} kms".format(round((W_WIDTH - 40) * PIXEL_SIZE, 8), round((W_WIDTH - 40) * PIXEL_SIZE, 8) * AU), True, (255, 255, 255))
    text2 = font.render("Time multiplier: {} second(s) for every passing second".format(TIME_MULTIPLIER), True, (255, 255, 255))
    text3 = font.render("Press Z to zoom in, X to zoom out, arrow keys to move the camera", True, (255, 255, 255))
    text4 = font.render("Camera is locked to the earth and moon initially", True, (255, 255, 255))
    caption = font.render("The Celestial Dance v0.1", True, (255, 255, 255))
    window.blit(caption, (20, 20))
    window.blit(text4, (20, W_HEIGHT - 108))
    window.blit(text3, (20, W_HEIGHT - 68))
    window.blit(text2, (20, W_HEIGHT - 88))
    window.blit(text, (20, W_HEIGHT - 48))

    #this whole section above is for the text at the bottom of the screen



    # oh my god. can you believe all the code above was for these two lines to work?
    # these two lines are the most important lines in this code. they make the planets move.
    # if you want to understand how this simulation works, follow the functions below where they take you.
    poses, vels = calculate_all_final_poses_and_vels(dt * TIME_MULTIPLIER)
    apply_final_poses_and_vels(poses, vels)



    pygame.display.flip()
    # screen update


    dt = clock.tick(1200)
    dt = decimal.Decimal(dt / 1000)
    ctr += 1

    # this is actually not the stupidest code i've ever written. i'm proud of myself.
    # but it is still stupid. i'm gonna go eat some ice cream now.
    # did i say this code is stupid? too stupid. oh my god. oh my god. help me.
    # end of the main loop

pygame.quit()

# goodbye.
# see you in the next code.
# now, how do i commit this to github?