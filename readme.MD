# AoE2 Minimap Generator
[![Python](https://img.shields.io/badge/Python-3.7.7-blue.svg)](https://www.python.org/)
[![Pillow](https://img.shields.io/badge/Pillow-8.0.0-green.svg)](https://pypi.org/project/Pillow/)
[![Mgz](https://img.shields.io/badge/Mgz-1.5.0-green.svg)](https://pypi.org/project/mgz/)

[![Screenshot](./screenshot_001.png)](https://github.com/Marfullsen/AoE2-minimap-generator)

## Description
Minimap generator from Age Of Empires 2 savegames.

## Features
- Vesion 0.2 works with .mgl, .mgx, .mgz and .aoe2record files.

## Dependencies
- [mgz](https://github.com/happyleavesaoc/aoc-mgz) (Also via pip: `pip install mgz`)
- [Pillow](https://pillow.readthedocs.io/en/stable/installation.html). (also via pip: `pip install Pillow`)

## Usage
Place the saved games in the same path as the Python script file, **after having installed the necessary dependencies**, run the Python script, voilà, map images will be generated, displayed and saved in the same directory.

## Installing Dependencies
Try these commands until you find one that works for you (this is because each linux distro is very picky), one of them should be suitable for you.
**Linux**
```
sudo pip3 install pillow
```
or
```
sudo python3 -m pip install pillow
```

**Windows**
```
pip install Pillow
```

## Tiles colors available.
Extracted from [recage/examples/map/terrainColors.json](https://github.com/genie-js/recage/blob/master/examples/map/terrainColors.json).

[![colors](./colors.png)](https://github.com/Marfullsen/AoE2-minimap-generator/blob/master/colors_available.py)

## TODO
:heavy_check_mark: Generate map from a saved game (.mgl, .mgx, .mgz and .aoe2record files).

:heavy_check_mark: Rotate the map and add transparency to the background.

:black_square_button: Put the gold and stone resources.

:black_square_button: Location of each player.

## Credits
Thanks to [aoc-mgz](https://github.com/happyleavesaoc/aoc-mgz) by [HappyLeavesAoC](https://github.com/happyleavesaoc/) for the extract functions.