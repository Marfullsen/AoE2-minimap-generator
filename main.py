#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob

from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from mgz.summary import Summary
from mgz.const import MAP_SIZES

map_sizes = dict(zip(MAP_SIZES.values(),MAP_SIZES.keys()))

player_colors = ('#0000DD', '#ff0000', '#00ff00', '#ffff00', '#00ffff', '#ff00ff', '#434343', '#ff8201')

def draw_point(img, x, y, color):
    color = player_colors[color]
    draw = ImageDraw.Draw(img)
    far = 6
    x1,y1,x2,y2 = (x-5, y-5, x+5, y+5)
    draw.ellipse((x1,y1, x2, y2), fill=color)
    draw.ellipse((x1-far,y1-far, x2+far, y2+far), outline=color, width=3)

def get_savedgames():
    recorded_games = []
    supported_extensions = ('.mgl', '.mgx', '.mgz', '.aoe2record')

    for recorded_game in range(len(supported_extensions)):
        if glob.glob('*'+supported_extensions[recorded_game]):
            recorded_games += glob.glob('*'+supported_extensions[recorded_game])
    return recorded_games

forty_colors = ['#339727', '#305db6', '#e8b478', '#e4a252', '#5492b0', '#339727', '#e4a252', '#82884d', '#82884d', '#339727', '#157615', '#e4a252', '#339727', '#157615', '#e8b478', '#305db6', '#339727', '#157615', '#157615', '#157615', '#157615', '#157615', '#004aa1', '#004abb', '#e4a252', '#e4a252', '#ffec49', '#e4a252', '#305db6', '#82884d', '#82884d', '#82884d', '#c8d8ff', '#c8d8ff', '#c8d8ff', '#98c0f0', '#c8d8ff', '#98c0f0', '#c8d8ff', '#c8d8ff', '#e4a252']

forty_rgb = []
for color in forty_colors:
    forty_rgb.append(color[1:])

def to_rgb(farbe: str) -> tuple(['rrr','ggg','bbb']):
    return tuple(int(farbe[i:i+2], 16) for i in (0, 2, 4))

def write_minimap(input_file: str) -> 'output file: {input_file}.png':
    global mapa, players, objects, header
    with open(f'{input_file}', 'rb') as data:
        summary = Summary(data)
        
    mapa = summary.get_map()
    players = summary.get_players()
    objects = summary.get_objects()
    header = summary.get_header()
        
    map_size = map_sizes[mapa['size']]
    TOTAL_TILES = map_size ** 2
    
    img = Image.new('RGBA', (map_size, map_size))
    final_image = Image.new("RGBA", (300,200), (0,0,0,0))
    
    x,y = (0,0)
    for i in range(TOTAL_TILES):
        x = mapa['tiles'][i]['x']
        y = mapa['tiles'][i]['y']
        terreno = mapa['tiles'][i]['terrain_id'] 
        img.putpixel((x,y), to_rgb((forty_colors[terreno])[1:]))

    resources = header['initial']['players'][0]['objects']
    for resource in resources:
        if resource['object_type'] in [59, 833, 594, 65, 48, 810, 1026, 822, 1031, 1139, 69, 455, 456, 458, 457, 450, 451, 452]: #A5C46C, Food: berry_bush, fish, other animals.
            img.putpixel( (int(resource['x']), int(resource['y'])), to_rgb('A5C46C'))
        if resource['object_type'] == 102: #919191, stone_pile
            img.putpixel( (int(resource['x']), int(resource['y'])), to_rgb('919191'))
        if resource['object_type'] == 66: #FFC700, gold_pile
            img.putpixel( (int(resource['x']), int(resource['y'])), to_rgb('FFC700'))
        if resource['object_type'] == 285: #FFF, Relic
            img.putpixel( (int(resource['x']), int(resource['y'])), to_rgb('FFFFFF'))
            img.putpixel( (int(resource['x']+1), int(resource['y'])), to_rgb('FFFFFF'))
            img.putpixel( (int(resource['x']), int(resource['y'])+1), to_rgb('FFFFFF'))
            img.putpixel( (int(resource['x']-1), int(resource['y'])), to_rgb('FFFFFF'))
            img.putpixel( (int(resource['x']), int(resource['y'])-1), to_rgb('FFFFFF'))
            
    for player in players:
        for coordinates in player:
            x = player['position'][0]
            y = player['position'][1]
            draw_point(img, x, y, player['color_id'])
            
    for obj in objects.get('objects'):
        if obj['object_id'] == 72: # Palisade wall.
            img.putpixel( (int(obj['x']), int(obj['y'])), to_rgb( player_colors[players[obj['player_number']-1]['color_id']][1:] ) )
            
        if obj['object_id'] == 117: # Stone wall.
            img.putpixel( (int(obj['x']), int(obj['y'])), to_rgb( player_colors[players[obj['player_number']-1]['color_id']][1:] ) )
            
        if obj['object_id'] == 155: # Fortified wall.
            img.putpixel( (int(obj['x']), int(obj['y'])), to_rgb( player_colors[players[obj['player_number']-1]['color_id']][1:] ) )
            
        if obj['object_id'] in [64, 81, 88, 95]: # Stone gate.
            img.putpixel( (int(obj['x']), int(obj['y'])), to_rgb( player_colors[players[obj['player_number']-1]['color_id']][1:] ) )
            
        if obj['object_id'] in [662, 666, 670, 674]: # Palisade gate.
            img.putpixel( (int(obj['x']), int(obj['y'])), to_rgb( player_colors[players[obj['player_number']-1]['color_id']][1:] ) )
            
    angle = 45
    rotated = img.rotate(angle, resample=Image.BICUBIC, expand=True)
    rotated = rotated.resize((int(map_size*1.5), map_size))
    
    final_image.paste(rotated, (0, 0), rotated)
    output_file_name = f'{input_file[:-4]}.png'
    final_image.save(output_file_name)
    final_image.show()
    
if __name__== "__main__":
    for rec in get_savedgames():
        write_minimap(rec)