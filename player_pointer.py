#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PIL import Image, ImageDraw

player_colors = ('#0000DD', '#ff0000', '#00ff00', '#ffff00', '#00ffff', '#ff00ff', '#434343', '#ff8201')

def draw_point(img, x, y, color):
    color = player_colors[color]
    draw = ImageDraw.Draw(img)
    far = 6
    x1,y1,x2,y2 = (x-5, y-5, x+5, y+5)
    draw.ellipse((x1,y1, x2, y2), fill=color)
    draw.ellipse((x1-far,y1-far, x2+far, y2+far), outline=color, width=3)

if __name__== "__main__":
    img = Image.open("recorded game -  06-abr-2021 23`22`35.png")
    draw_point(img, 112, 171, 0)
    draw_point(img, 91, 44, 1)
    draw_point(img, 188, 51, 2)

    draw_point(img, 39, 67, 4)
    draw_point(img, 40, 148,5)
    draw_point(img, 155, 123, 6)

    img.save("mapa3.png")
    img.show()
