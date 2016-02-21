import bottle
import os
import random

directions = ['north','east','south','west']

debug = True

def is_valid(request,move):
    """
    Maybe instead of checking what's false, check what's true
    """
    move_coords = get_direction(move)

    us = get_our_snake(request)
    our_head = us['coords'][0]

    if debug:
        print("us: {}".format(us))

    for snake in request['snakes']:
      if(our_head[1]+1 + move_coords[1] == snake['coords'][1] or our_head[1]-1 + move_coords[1] == snake['coords'][1]):
        return False
      if(our_head[0]+1 + move_coords[0] == snake['coords'][0] or our_head[1]-1 + move_coords[1] == snake['coords'][0]):
        return False

    # north wall
    if (move == 'north'):
        if(our_head[1] + move_coords[1] <= 0):
            return False			  

    # east wall    
    if (move == 'east'):
      if(our_head[0] + move_coords[0] >= (request['width'] - 1)):
        return False
    
    # south wall
    if (move == 'south'):
        if(our_head[1] + move_coords[1] >= (request['height'] - 1)):
           return False
       
    # west wall
    if (move == 'west'):
        if (our_head[0] + move_coords[0] <= 0):
            return False

    return True

def get_direction(move):
    return {
        'north' : [0,-1],
        'south' : [0,1],
        'west' : [-1,0],
        'east' : [1,0]
    }.get(move,'north')


def valid_moves(request):
    good = []
    for move in directions:
        if is_valid(request,move):
            good.append(move)
    return good
        
def get_our_head(request):
    """
    We should depricated this and use only get_our_snake
    """
    for snake in request['snakes']:
        if snake['name'] == 'OObuddies':
            return snake['coords'][0]
      
def get_our_snake(request):
    for snake in request['snakes']:
        if snake['name'] == 'OObuddies':
            return snake

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

def is_hungry(request):
    if request['health'] <= 50:
        return True
    return False

def get_taunt():
    taunts = ['Lean on me', 'Who has food?', 'I got this boiiizzzz', '#SnakeLife', 'You crawl here often?','Dayyyynk Lmao']
    random.shuffle(taunts)
    return taunts.pop()


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = 'http://i.imgur.com/K943feA.png'

    return {
        'color': '#00ff00',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json
    
    return {
        'taunt': get_taunt()
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    available = valid_moves(data)
  
    random.shuffle(available)
  
    return {
        'move': available[0],
        'taunt': get_taunt()
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    return {
        'taunt': get_taunt()
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
