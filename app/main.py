import bottle
import os
import random

from pprint import (pprint)

from bs_globals import *

from gets import *
from checks import *


def valid_moves(request):
    good = []

    us = get_our_snake(request)
    our_head = us['coords'][0]

    list_of_moves = get_possible_move_points(our_head)

    for move in directions:
        if is_valid(request,move):
            good.append(move)

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

    board_size = { 'min_x': 0, 'min_y': 0, 'max_x': data['width'], 'max_y': data['height'] }

    if debug:
        print("board size: {}\n".format(board_size))

    return {
        'taunt': 'glhf'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    available = valid_moves(data)

    invalid_moves = get_invalid_move_points(data)

    if debug:
        print("available moves: {}".format(available))

    if (len(available) == 4):
        print("problem, available move set has 4\n")

    random.shuffle(available)

    print("move: {}".format(available[0]))

    return {
        'move': available[0],
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
