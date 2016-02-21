import bottle
import os

def is_valid(request,move):
    move_coords = get_direction(move)
#replace 1 with our snake's head coordinates
    if (1 + move_coords[0] == request['width']):
        return False

    if (1 + move_coords[1] == request['height']):
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
    directions = {'north','south','west','east'}
    for move in directions:
        if not is_valid(request,move):
           directions.discard(move)
    return directions


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00ff00',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    print(data['width'], data['height'])
    # TODO: Do things with data

    return {
        'move': 'north',
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
