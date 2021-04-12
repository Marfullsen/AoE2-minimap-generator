#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PIL import Image, ImageDraw

colores_hex = iter(['#82884d', '#157615', '#5492b0', '#305db6', '#004aa1', '#339727', '#e4a252', '#e8b478', '#98c0f0', '#ffec49', '#004abb', '#c8d8ff'])

img = Image.new('RGBA', (330, 440), (0,0,0,0))
draw = ImageDraw.Draw(img)

def draw_point(x1, y1, x2, y2, color):
    draw.ellipse((x1,y1, x2, y2), fill=color)
    draw.ellipse((x1-20,y1-20, x2+20, y2+20), outline=color, width=10)

for i in range(3):
    for j in range(4):
        draw_point(21+(i*110), 21+(j*110), 79+(i*110), 79+(j*110),next(colores_hex))

img.save("colors.png")
img.show()
