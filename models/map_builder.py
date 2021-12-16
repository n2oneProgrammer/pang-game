import json
import os
from typing import List

import pymunk
from pygame.math import Vector2

from models.objects.physic_objects import PhysicObject
from models.objects.rectangle import Rectangle
from models.objects.sprite import Sprite


class MapBuilder:
    def __init__(self, src_map):
        self.src_map = os.path.join("maps", src_map)
        self.assets = []

    def get_elements(self, space) -> List[PhysicObject]:
        self.load_assets()
        with open(self.src_map, "r") as map_source_file:
            map_source = json.load(map_source_file)
            elements: List[PhysicObject] = []
            if "map" in map_source:
                for element in map_source["map"]:
                    elements.extend(self.construct_object(element, space))

                return elements
            else:
                raise ValueError("Map JSON must have map(list of elements on the map)")

    def load_assets(self):
        with open(self.src_map, "r") as map_source_file:
            map_source = json.load(map_source_file)
            self.assets = []
            if "assets" in map_source:
                for asset in map_source["assets"]:
                    self.assets.append(self.construct_asset(asset))

    @staticmethod
    def construct_asset(asset_json) -> object:
        if "name" not in asset_json or type(asset_json["name"]) is not str:
            raise ValueError("Assert object must have name")
        if "src" not in asset_json or type(asset_json["src"]) is not str:
            raise ValueError("Assert object must have src (path to image)")

        if not os.path.exists(os.path.join("assets", asset_json["src"])):
            raise FileNotFoundError(f"I cant find {asset_json['src']}")
        return asset_json

    def construct_object(self, object_json, space) -> List[PhysicObject]:
        if "type" not in object_json:
            raise ValueError("Object must have type")
        if "size" not in object_json:
            raise ValueError("Object Sprite must have size")

        if "stretch" in object_json and object_json["stretch"]:
            if "start-position" not in object_json:
                raise ValueError(
                    "Object with attribute stretch must have start-position"
                )

            if "end-position" not in object_json:
                raise ValueError("Object with attribute stretch must have end-position")
            result_list = []
            start_position_x = int(object_json["start-position"][0])
            start_position_y = int(object_json["start-position"][1])
            end_position_x = int(object_json["end-position"][0])
            end_position_y = int(object_json["end-position"][1])
            x_positions_list = [start_position_x] + list(
                range(
                    start_position_x + object_json["size"][0],
                    end_position_x,
                    object_json["size"][0],
                )
            )
            y_positions_list = [start_position_y] + list(
                range(
                    start_position_y + object_json["size"][1],
                    end_position_y,
                    object_json["size"][1],
                )
            )
            for x_stretch in x_positions_list:
                for y_stretch in y_positions_list:
                    object_json["position"] = [x_stretch, y_stretch]
                    result_list.append(self._construct_1_object(object_json, None))

            body = pymunk.Body()
            body.position = [(start_position_x + end_position_x + object_json["size"][0]) / 2,
                             (start_position_y + end_position_y + object_json["size"][1]) / 2]
            body.body_type = pymunk.Body.STATIC
            poly = pymunk.Poly.create_box(body,
                                          size=(
                                              end_position_x - start_position_x + object_json["size"][0],
                                              end_position_y - start_position_y + object_json["size"][1]
                                          ))
            poly.mass = 10
            poly.elasticity = 1
            poly.friction = 0

            space.add(body, poly)
            return result_list

        if "position" not in object_json:
            raise ValueError(f"Object {object_json['type']} must have position")

        return [self._construct_1_object(object_json, space)]

    def _construct_1_object(self, object_json, space):
        method_name = f"_construct_{object_json['type']}"
        method = getattr(self, method_name, self._not_implemented)
        return method(object_json, space)

    def _get_asset(self, name_asset):
        for asset in self.assets:
            if asset["name"] == name_asset:
                return asset
        return None

    def get_background(self):
        pass

    def _not_implemented(self, object_json, space):
        raise NotImplementedError(f"Type {object_json['type']} is not Implemented")

    def _construct_sprite(self, object_json, space) -> PhysicObject:
        if "asset" not in object_json:
            raise ValueError("Object Sprite must have asset(name to asset)")

        asset = self._get_asset(object_json["asset"])
        if asset is None:
            raise ValueError(f"Not found asset {object_json['asset']}")
        return Sprite(
            path=asset['src'],
            position=Vector2(object_json["position"]),
            width=object_json["size"][0],
            height=object_json["size"][1],
            space=space
        )

    def _construct_rect(self, object_json, space) -> PhysicObject:
        if "color" not in object_json:
            raise ValueError("Object Sprite must have color(in format #000000)")
        return Rectangle(
            position=Vector2(object_json["position"]),
            width=object_json["size"][0],
            height=object_json["size"][1],
            color=object_json["color"],
            space=space
        )
