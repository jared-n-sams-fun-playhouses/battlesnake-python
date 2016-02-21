import bottle
import os
import random

from pprint import (pprint)

from bs_globals import *

from gets import *
from checks import *

last_location = None

def valid_moves(request):
    good = []

    us = get_our_snake(request)
    our_head = us['coords'][0]

    print("head coord: {}".format(our_head))

    list_of_moves = get_possible_move_points(our_head)

    print("list of moves: {}".format(list_of_moves))

    for direction, point in list_of_moves.items():
        #print("{}: {}: {}".format(direction, point, is_edge(point)))
        if (is_edge(direction, point, { 'min_x': 0, 'min_y': 0, 'max_x': request['width'], 'max_y': request['height'] })):
            print("{}: is edge".format(direction))

    for move in directions:
        if is_valid(request,move):
            good.append(move)

    if debug:
        print("available moves: {}".format(good))
        if (len(good) == 4):
            print("problem, valid move set has 4, needs to less than 4")

    return good


"""
Main Functions
"""
@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = 'http://i.imgur.com/K943feA.png'

    return {
        'color': '#f0f0f0',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    #if debug:
    #    print("board size: {}\n".format(board_size))

    return {
        'taunt': 'glhf'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    available = valid_moves(data)

    invalid_moves = get_invalid_move_points(data)

    random.shuffle(available)

    print("move: {}".format(available[0]))

    print("turn: {}".format(data['turn']))

    us = get_our_snake(data)
    our_head = us['coords'][0]
    print("head: {}".format(our_head))

    return {
        'move': 'south',
        'taunt': get_taunt()
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    return {
        'taunt': 'gg'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
