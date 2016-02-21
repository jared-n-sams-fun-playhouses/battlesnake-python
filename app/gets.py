import random

from bs_globals import *

def get_taunt():
    taunts = ['Lean on me', 'Who has food?', 'I got this boiiizzzz', '#SnakeLife', 'You crawl here often?','Dayyyynk Lmao']
    random.shuffle(taunts)
    return taunts.pop()


def get_directions(move):
    return {
        'north' : [0,-1],
        'south' : [0,1],
        'west' : [-1,0],
        'east' : [1,0]
    }.get(move,'north')


def get_food_coord(request):
    location = get_our_head(request)
    lowest = 100

    for food in request['food']:
        headtotal = location[0] - location[1]
        food_total = food[0] - food[1]
        diff = head_total - food_total

        if diff < lowest:
            lowest = diff
            closest_food = food

    return closest_food


def get_our_snake(request):
    for snake in request['snakes']:
        if snake['name'] == 'OObuddies':
            return snake


def get_possible_move_points(coord):
    """
    Coord is a relative point
    """
    return {
        'north': [ (coord[0]), (coord[1] - 1) ],
        'south': [ (coord[0]), (coord[1] + 1) ],
        'east' : [ (coord[0] + 1), (coord[1]) ],
        'west' : [ (coord[0] - 1), (coord[1]) ]
    }


def get_invalid_move_points(request):
    no_good = []

    for snake in request['snakes']:
        for coord in snake['coords']:
            no_good.append(coord)

    if debug:
        print("invalid points: {}".format(no_good))

    return no_good
