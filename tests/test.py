#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob
from mgz.summary import Summary

input_file = glob.glob('*.mgx')[0]

with open(f'{input_file}', 'rb') as data:
    sumario = Summary(data)
mapa = sumario.get_map()
players = sumario.get_players()
objects = sumario.get_objects()
header = sumario.get_header()

walls = 0
gates = 0
cliffs = 0
for obj in objects.get('objects'):
    if obj['object_id'] == 72: # Palisade wall.
        walls += 1
    if obj['object_id'] == 117: # Stone wall.
        walls += 1
    if obj['object_id'] == 155: # Fortified wall.
        walls += 1
    if obj['object_id'] in [64, 81, 88, 95]: # Stone gate.
        gates += 1
    if obj['object_id'] in [662, 666, 670, 674]: # Palisade gate.
        gates += 1
    if obj['object_id'] in [264, 265, 266, 267, 268, 269, 270, 271, 272, 273]: # Cliffs
        cliffs += 1

print(f'total murallas {walls}')
print(f'total Puertas {gates//3}')
print(f'total acantilados {cliffs}')
