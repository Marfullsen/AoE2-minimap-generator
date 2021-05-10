#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob

from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from mgz.summary import Summary
from mgz.const import MAP_SIZES

map_sizes = dict(zip(MAP_SIZES.values(),MAP_SIZES.keys()))
player_colors = ('#0000DD', '#ff0000', '#00ff00', '#ffff00', '#00ffff', '#ff00ff', '#E9E9E9', '#ff8201')

def draw_point(canvas, x, y, color):
    '''Points the initial player position with a special large circle'''
    player_color = player_colors[color]
    x1,y1,x2,y2 = (x-5, y-5, x+5, y+5)
    draw = ImageDraw.Draw(canvas)
    far = 6
    draw.ellipse((x1,y1, x2, y2), fill=player_color)
    draw.ellipse((x1-far,y1-far, x2+far, y2+far), outline=player_color, width=3)

def get_savedgames() -> ['recordedgames_file_names.valid_extension']:
    '''Gets file names with valid extensions'''
    recorded_games = []
    supported_extensions = ('.mgl', '.mgx', '.mgz', '.aoe2record')
    for recorded_game in range(len(supported_extensions)):
        if glob.glob('*'+supported_extensions[recorded_game]):
            recorded_games += glob.glob('*'+supported_extensions[recorded_game])
    return recorded_games

def to_rgb(farbe: str) -> tuple(['rrr','ggg','bbb']):
    '''Transforms an hex color value to a rgb color value'''
    return tuple(int(farbe[i:i+2], 16) for i in (0, 2, 4))

def get_data_from(input_file: str):
    '''Gets a summary'''
    with open(f'{input_file}', 'rb') as data:
        return Summary(data)

def new_canvas(map_size):
    return Image.new('RGBA', (map_size, map_size))

def draw_terrain(canvas, map_info, total_tiles):
    tiles_colors = ('#339727', '#305db6', '#e8b478', '#e4a252', '#5492b0',
                    '#339727', '#e4a252', '#82884d', '#82884d', '#339727',
                    '#157615', '#e4a252', '#339727', '#157615', '#e8b478',
                    '#305db6', '#339727', '#157615', '#157615', '#157615',
                    '#157615', '#157615', '#004aa1', '#004abb', '#e4a252',
                    '#e4a252', '#ffec49', '#e4a252', '#305db6', '#82884d',
                    '#82884d', '#82884d', '#c8d8ff', '#c8d8ff', '#c8d8ff',
                    '#98c0f0', '#c8d8ff', '#98c0f0', '#c8d8ff', '#c8d8ff',
                    '#e4a252')
    x,y = (0,0)
    for i in range(total_tiles):
        x = map_info['tiles'][i]['x']
        y = map_info['tiles'][i]['y']
        terrain = map_info['tiles'][i]['terrain_id'] 
        canvas.putpixel((x,y), to_rgb((tiles_colors[terrain])[1:]))

def draw_resources(canvas, resources):
    for resource in resources:
        if resource['object_type'] in [59, 833, 594, 65, 48, 810, 1026, 822, 1031, 1139, 69, 455, 456, 458, 457, 450, 451, 452]: # Food: berry_bush, fish, other animals.
            canvas.putpixel( (int(resource['x']), int(resource['y'])), to_rgb('A5C46C'))
            
        if resource['object_type'] == 102: # Stone pile
            canvas.putpixel( (int(resource['x']), int(resource['y'])), to_rgb('919191'))
            
        if resource['object_type'] == 66: # Gold pile
            canvas.putpixel( (int(resource['x']), int(resource['y'])), to_rgb('FFC700'))
            
        if resource['object_type'] == 285: # Relic
            canvas.putpixel( (int(resource['x']), int(resource['y'])), to_rgb('FFFFFF'))
            canvas.putpixel( (int(resource['x']+1), int(resource['y'])), to_rgb('FFFFFF'))
            canvas.putpixel( (int(resource['x']), int(resource['y'])+1), to_rgb('FFFFFF'))
            canvas.putpixel( (int(resource['x']-1), int(resource['y'])), to_rgb('FFFFFF'))
            canvas.putpixel( (int(resource['x']), int(resource['y'])-1), to_rgb('FFFFFF'))

def draw_players(canvas, players):
    for player in players:
        for coordinates in player:
            x = player['position'][0]
            y = player['position'][1]
            draw_point(canvas, x, y, player['color_id'])

def draw_walls(canvas, objects, players):
    '''Draws the walls according to:
        72 -> Palisade wall.
        117 -> Stone wall.
        155 -> Fortified wall.
        64, 81, 88, 95 -> Stone gate.
        662, 666, 670, 674 -> Palisade gate.
    '''
    for obj in objects.get('objects'):
        if obj['object_id'] in [72, 117, 155, 64, 81, 88, 95, 662, 666, 670, 674]:
            canvas.putpixel( (int(obj['x']), int(obj['y'])), to_rgb(player_colors[players[obj['player_number']-1]['color_id']][1:]))

def get_image(canvas, output_file_name):
    final_image = Image.new("RGBA", (300,200), (0,0,0,0))
    final_image.paste(canvas, (0, 0), canvas)
    final_image.save(output_file_name)
    return final_image

def rotate(canvas, angle):
    return canvas.rotate(angle, resample=Image.BICUBIC, expand=True)

def resize(canvas, size):
    return canvas.resize(size)

def write_minimap(input_file: str) -> 'minimap_{file_name}.png':
    '''Generates the minimap'''
    summary = get_data_from(input_file)
    resources = summary.get_header()['initial']['players'][0]['objects']
    map_info = summary.get_map()
    players = summary.get_players()
    objects = summary.get_objects()
    
    map_size = map_sizes[map_info['size']]
    canvas = new_canvas(map_size)
    total_tiles = map_size ** 2
    
    draw_terrain(canvas, map_info, total_tiles)
    draw_resources(canvas, resources)
    draw_players(canvas, players)
    draw_walls(canvas, objects, players)

    angle = 45
    canvas = rotate(canvas, angle)
    canvas = resize(canvas, (300,200))

    output_file_name = f'minimap_{input_file[:-4]}.png'
    minimap = get_image(canvas, output_file_name)
    minimap.show()
    
if __name__== "__main__":
    for rec in get_savedgames():
        write_minimap(rec)
