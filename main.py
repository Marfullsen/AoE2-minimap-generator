#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import logging

from PIL import Image, ImageDraw

from mgz.summary import Summary
from mgz.reference import get_dataset
from mgz.util import Version

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOG = logging.getLogger("minimap")

PLAYER_COLORS = (
    "#0000DD", "#ff0000", "#00ff00", "#ffff00",
    "#00ffff", "#ff00ff", "#E9E9E9", "#ff8201",
)

FALLBACK_TERRAIN_COLOR = "#555555"

FOOD_OBJECT_IDS = {
    59,   # Forage Bush
    833,  # Turkey
    594,  # Sheep
    65, 333,   # Deer (two variants)
    48,   # Wild Boar
    810,  # Iron Boar
    1026,  # Ostrich
    822,  # Javelina
    1031,  # Crocodile
    1139,  # Rhinoceros
    69,   # Shore Fish
    455, 456, 457, 458, 450, 451, 452,  # Fish variants + Great Fish (Marlin)
    53,   # Fish (Perch)
    1060,  # Goat
    1239,  # Ibex
    1019,  # Zebra
    305,  # Llama
    936, 1301,  # Elephant (wild/huntable, not War/Battle Elephant units)
}
STONE_OBJECT_IDS = {102, 839}   # Stone Mine, Rock (Stone)
GOLD_OBJECT_IDS = {66, 841}     # Gold Mine, Rock (Gold)
RELIC_OBJECT_IDS = {285}        # Relic
WALL_OBJECT_IDS = {
    72, 117, 155,          # Palisade / Stone / Fortified wall
    64, 81, 88, 95,        # Stone gates
    662, 666, 670, 674,    # Palisade gates
}


def to_rgb(hex_color: str) -> tuple:
    """Transforms a hex color value (with or without leading #) to RGB."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def load_terrain_colors() -> dict:
    """Builds a terrain_id -> RGB color table from the reference dataset
    bundled with mgz."""
    try:
        _, dataset = get_dataset(Version.DE, [])
        return {
            int(terrain_id): to_rgb(info["colors"]["level"])
            for terrain_id, info in dataset["terrain"].items()
        }
    except Exception as exc:  # pylint: disable=broad-except
        LOG.warning("Could not load terrain reference data (%s); "
                    "falling back to a single flat color for all terrain.", exc)
        return {}


TERRAIN_COLORS = load_terrain_colors()
_warned_terrain_ids = set()


def get_savedgames() -> list:
    """Gets file names with valid extensions in the current directory."""
    supported_extensions = (".mgl", ".mgx", ".mgz", ".aoe2record")
    recorded_games = []
    for ext in supported_extensions:
        recorded_games += glob.glob("*" + ext)
    return recorded_games


def get_data_from(input_file: str):
    """Parses a savegame. Returns either a ModelSummary or a FullSummary
    depending on the file - see the module docstring for why that matters."""
    with open(input_file, "rb") as data:
        return Summary(data)


def is_model_summary(summary) -> bool:
    return hasattr(summary, "match")


def extract_match_data(summary):
    if is_model_summary(summary):
        match = summary.match
        map_info = dict(
            dimension=match.map.dimension,
            tiles=[
                dict(x=tile.position.x, y=tile.position.y, terrain_id=tile.terrain)
                for tile in match.map.tiles
            ],
        )
        players = [
            dict(position=(p.position.x, p.position.y), color_id=p.color_id)
            for p in match.players
        ]
        resource_objects = [
            (obj.object_id, obj.position.x, obj.position.y) for obj in match.gaia
        ]
        wall_objects = []
        for player in match.players:
            for obj in player.objects:
                wall_objects.append(
                    (obj.object_id, obj.position.x, obj.position.y, player.number)
                )
    else:
        map_info = summary.get_map()
        players = summary.get_players()
        header = summary.get_header()
        resource_objects = [
            (obj["object_type"], obj["x"], obj["y"])
            for obj in header["initial"]["players"][0]["objects"]
        ]
        objects = summary.get_objects()
        wall_objects = [
            (obj["object_id"], obj["x"], obj["y"], obj["player_number"])
            for obj in objects.get("objects", [])
        ]
    return map_info, players, resource_objects, wall_objects


def draw_point(canvas, x, y, color_id):
    """Points the initial player position with a special large circle."""
    player_color = PLAYER_COLORS[color_id]
    x1, y1, x2, y2 = (x - 5, y - 5, x + 5, y + 5)
    draw = ImageDraw.Draw(canvas)
    far = 6
    draw.ellipse((x1, y1, x2, y2), fill=player_color)
    draw.ellipse((x1 - far, y1 - far, x2 + far, y2 + far), outline=player_color, width=3)


def new_canvas(map_size):
    return Image.new("RGBA", (map_size, map_size))


def draw_terrain(canvas, map_info):
    for tile in map_info["tiles"]:
        terrain_id = tile["terrain_id"]
        color = TERRAIN_COLORS.get(terrain_id)
        if color is None:
            if terrain_id not in _warned_terrain_ids:
                LOG.warning("Unrecognized terrain_id %s; using fallback color "
                            "(update mgz/aocref if this keeps happening).", terrain_id)
                _warned_terrain_ids.add(terrain_id)
            color = to_rgb(FALLBACK_TERRAIN_COLOR)
        canvas.putpixel((tile["x"], tile["y"]), color)


def draw_resources(canvas, resource_objects):
    for object_id, x, y in resource_objects:
        x, y = int(x), int(y)
        if object_id in FOOD_OBJECT_IDS:
            canvas.putpixel((x, y), to_rgb("A5C46C"))
        elif object_id in STONE_OBJECT_IDS:
            canvas.putpixel((x, y), to_rgb("919191"))
        elif object_id in GOLD_OBJECT_IDS:
            canvas.putpixel((x, y), to_rgb("FFC700"))
        elif object_id in RELIC_OBJECT_IDS:
            for dx, dy in ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)):
                canvas.putpixel((x + dx, y + dy), to_rgb("FFFFFF"))


def draw_players(canvas, players):
    for player in players:
        x, y = player["position"]
        draw_point(canvas, x, y, player["color_id"])


def draw_walls(canvas, wall_objects, players):
    """Draws walls/gates, colored by owning player.
    Skips Gaia-owned objects (player_number 0) and any out-of-range
    player_number."""
    for object_id, x, y, player_number in wall_objects:
        if object_id not in WALL_OBJECT_IDS:
            continue
        if player_number <= 0 or player_number > len(players):
            continue
        color = PLAYER_COLORS[players[player_number - 1]["color_id"]]
        canvas.putpixel((int(x), int(y)), to_rgb(color[1:]))


def get_image(canvas, output_file_name):
    final_image = Image.new("RGBA", (300, 200), (0, 0, 0, 0))
    final_image.paste(canvas, (0, 0), canvas)
    final_image.save(output_file_name)
    return final_image


def rotate(canvas, angle):
    return canvas.rotate(angle, resample=Image.BICUBIC, expand=True)


def resize(canvas, size):
    return canvas.resize(size)


def write_minimap(input_file: str):
    """Generates the minimap."""
    summary = get_data_from(input_file)
    map_info, players, resource_objects, wall_objects = extract_match_data(summary)

    canvas = new_canvas(map_info["dimension"])

    draw_terrain(canvas, map_info)
    draw_resources(canvas, resource_objects)
    draw_players(canvas, players)
    draw_walls(canvas, wall_objects, players)

    canvas = rotate(canvas, 45)
    canvas = resize(canvas, (300, 200))
    output_file_name = f"minimap_{input_file[:-4]}.png"
    minimap = get_image(canvas, output_file_name)
    minimap.show()


if __name__ == "__main__":
    saved_games = get_savedgames()
    if not saved_games:
        LOG.warning("No .mgl/.mgx/.mgz/.aoe2record files found in this folder.")
    for rec in saved_games:
        try:
            write_minimap(rec)
            LOG.info("Generated minimap for %s", rec)
        except Exception as exc:  # pylint: disable=broad-except
            LOG.error("Failed on %s: %s", rec, exc)