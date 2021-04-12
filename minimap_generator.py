#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob

from PIL import Image
from PIL import ImageColor
from mgz.summary import Summary
from mgz.const import MAP_SIZES

map_sizes = dict(zip(MAP_SIZES.values(),MAP_SIZES.keys()))
mgx_file = glob.glob('*.mgx')[0]

with open(f'{mgx_file}', 'rb') as data:
    s = Summary(data)
    mapa = s.get_map()

dic_colores = {'#339727': (51, 151, 39), '#305db6': (48, 93, 182), '#e8b478': (232, 180, 120), '#e4a252': (228, 162, 82), '#5492b0': (84, 146, 176), '#82884d': (130, 136, 77), '#157615': (21, 118, 21), '#004aa1': (0, 74, 161), '#004abb': (0, 74, 187), '#ffec49': (255, 236, 73), '#c8d8ff': (200, 216, 255), '#98c0f0': (152, 192, 240)}
colores_hex = ['#82884d', '#157615', '#5492b0', '#305db6', '#004aa1', '#339727', '#e4a252', '#e8b478', '#98c0f0', '#ffec49', '#004abb', '#c8d8ff']
farben = [(130, 136, 77), (21, 118, 21), (84, 146, 176), (48, 93, 182), (0, 74, 161), (51, 151, 39), (228, 162, 82), (232, 180, 120), (152, 192, 240), (255, 236, 73), (0, 74, 187), (200, 216, 255)]
forty_colors = ['#339727', '#305db6', '#e8b478', '#e4a252', '#5492b0', '#339727', '#e4a252', '#82884d', '#82884d', '#339727', '#157615', '#e4a252', '#339727', '#157615', '#e8b478', '#305db6', '#339727', '#157615', '#157615', '#157615', '#157615', '#157615', '#004aa1', '#004abb', '#e4a252', '#e4a252', '#ffec49', '#e4a252', '#305db6', '#82884d', '#82884d', '#82884d', '#c8d8ff', '#c8d8ff', '#c8d8ff', '#98c0f0', '#c8d8ff', '#98c0f0', '#c8d8ff', '#c8d8ff', '#e4a252']
forty_rgb = []
# ['339727', '305db6', 'e8b478', 'e4a252', '5492b0', '339727', 'e4a252', '82884d', '82884d', '339727', '157615', 'e4a252', '339727', '157615', 'e8b478', '305db6', '339727', '157615', '157615', '157615', '157615', '157615', '004aa1', '004abb', 'e4a252', 'e4a252', 'ffec49', 'e4a252', '305db6', '82884d', '82884d', '82884d', 'c8d8ff', 'c8d8ff', 'c8d8ff', '98c0f0', 'c8d8ff', '98c0f0', 'c8d8ff', 'c8d8ff', 'e4a252']

def to_rgb(farbe):
    return tuple(int(farbe[i:i+2], 16) for i in (0, 2, 4))

for color in forty_colors:
    forty_rgb.append(color[1:])

def write_minimap():
    MAP_SIZE = map_sizes[mapa['size']]
    TOTAL_TILES = MAP_SIZE ** 2
    img = Image.new('RGB', (MAP_SIZE, MAP_SIZE))
    x,y = (0,0)
    #all_tiles = list()
    for i in range(TOTAL_TILES):
        x = mapa['tiles'][i]['x']
        y = mapa['tiles'][i]['y']
        terreno = mapa['tiles'][i]['terrain_id'] 
        img.putpixel((x,y), to_rgb((forty_colors[terreno])[1:]))
    ANGLE = 45
    img = img.rotate(ANGLE, expand=True)
    img = img.resize((int(MAP_SIZE*1.5), MAP_SIZE))
    output_file_name = f'{mgx_file[:-4]}.png'
    img.save(output_file_name)
    img.show()


write_minimap()
