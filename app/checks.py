from bs_globals import *

from gets import *

def new_is_valid(coord):
    if (coord[0] <= 0):
        return False


def is_edge(direction, vertex, board_bounds):
    for key, value in board_bounds.items():
        print(vertex)
        print("{} {}".format(key,value))
        # north
        if (direction == 'north' and key == 'min_y' and vertex[1] <= value):
            return True
        # south
        elif (direction == 'south' and key == 'max_y' and vertex[1] >= value):
            return True
        # east
        elif (direction == 'east' and key == 'max_x' and vertex[0] >= value):
            return True
        # west
        elif (direction == 'west' and key == 'min_x' and vertex[0] <= value):
            return True

    return False


def is_hungry(request):
    if request['health'] <= 50:
        return True

    return False


def is_valid(request, move):
    """
    Maybe instead of checking what's false, check what's true
    """
    move_coords = get_directions(move)

    us = get_our_snake(request)
    our_head = us['coords'][0]

    for snake in request['snakes']:
      if(our_head[1]+1 + move_coords[1] == snake['coords'][1] or our_head[1]-1 + move_coords[1] == snake['coords'][1]):
        return False
      if(our_head[0]+1 + move_coords[0] == snake['coords'][0] or our_head[1]-1 + move_coords[1] == snake['coords'][0]):
        return False

    # north wall
    if (move == 'north'):
        if(our_head[1] + move_coords[1] < 0):
            return False

    # east wall
    if (move == 'east'):
      if(our_head[0] + move_coords[0] > (request['width'] - 1)):
        return False

    # south wall
    if (move == 'south'):
        if(our_head[1] + move_coords[1] > (request['height'] - 1)):
           return False

    # west wall
    if (move == 'west'):
        if (our_head[0] + move_coords[0] < 0):
            return False

    return True
