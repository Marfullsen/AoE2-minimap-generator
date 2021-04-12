#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob

from PIL import Image
from PIL import ImageColor
from mgz.summary import Summary
from mgz.const import MAP_SIZES

map_sizes = dict(zip(MAP_SIZES.values(),MAP_SIZES.keys()))

recorded_games = []
supported_extensions = ('.mgl', '.mgx', '.mgz', '.aoe2record')

for recorded_game in range(len(supported_extensions)):
    if glob.glob('*'+supported_extensions[recorded_game]):
        recorded_games += glob.glob('*'+supported_extensions[recorded_game])

forty_colors = ['#339727', '#305db6', '#e8b478', '#e4a252', '#5492b0', '#339727', '#e4a252', '#82884d', '#82884d', '#339727', '#157615', '#e4a252', '#339727', '#157615', '#e8b478', '#305db6', '#339727', '#157615', '#157615', '#157615', '#157615', '#157615', '#004aa1', '#004abb', '#e4a252', '#e4a252', '#ffec49', '#e4a252', '#305db6', '#82884d', '#82884d', '#82884d', '#c8d8ff', '#c8d8ff', '#c8d8ff', '#98c0f0', '#c8d8ff', '#98c0f0', '#c8d8ff', '#c8d8ff', '#e4a252']

forty_rgb = []
for color in forty_colors:
    forty_rgb.append(color[1:])

def to_rgb(farbe: str) -> tuple(['rrr','ggg','bbb']):
    return tuple(int(farbe[i:i+2], 16) for i in (0, 2, 4))

def write_minimap(input_file: str) -> 'output file: {input_file}.png':
    with open(f'{input_file}', 'rb') as data:
        mapa = Summary(data).get_map()
        
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
        
    angle = 45
    rotated = img.rotate(angle, resample=Image.BICUBIC, expand=True)
    rotated = rotated.resize((int(map_size*1.5), map_size))
    
    final_image.paste(rotated, (0, 0), rotated)
    output_file_name = f'{input_file[:-4]}.png'
    final_image.save(output_file_name)
    final_image.show()

# Test
for rec in recorded_games:
    write_minimap(rec)
