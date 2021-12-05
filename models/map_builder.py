import os
from typing import List

from pygame.math import Vector2

from models.objects.physic_objects import PhysicObject
from models.objects.rectangle import Rectangle


class MapBuilder:
    def __init__(self, src_map):
        self.src_map = src_map
        self.assets = []

    def get_elements(self):
        pass

    def load_assets(self):
        pass

    @staticmethod
    def construct_asset(asset_json) -> object:
        if "name" not in asset_json or type(asset_json["name"]) is not str:
            raise ValueError("Assert object must have name")
        if "src" not in asset_json or type(asset_json["src"]) is not str:
            raise ValueError("Assert object must have src (path to image)")

        asset_json["src"] = os.path.join("assets", asset_json["src"])
        if not os.path.exists(asset_json["src"]):
            raise FileNotFoundError(f"I cant find {asset_json['src']}")
        return asset_json

    def construct_object(self, object_json) -> List[PhysicObject]:
        if "type" not in object_json:
            raise ValueError("Object must have type")

        if object_json["type"] == "sprite":
            if "asset" not in object_json:
                raise ValueError("Object Sprite must have asset(name to asset)")
            if "position" not in object_json:
                raise ValueError("Object Sprite must have position")
            if "size" not in object_json:
                raise ValueError("Object Sprite must have size")
            return [self._construct_sprite_object(object_json["asset"], object_json["position"], object_json["size"])]
        if object_json["type"] == "rect":
            if "color" not in object_json:
                raise ValueError("Object Sprite must have color(in format #000000)")
            if "position" not in object_json:
                raise ValueError("Object Sprite must have position")
            if "size" not in object_json:
                raise ValueError("Object Sprite must have size")
            return [self._construct_sprite_type(object_json['color'], object_json['position'], object_json['size'])]
        raise NotImplementedError(f"Type object_json['type'] is not Implemented")

    def get_background(self):
        pass

    @staticmethod
    def _construct_sprite_object(asset: str, position: Vector2, size: Vector2) -> PhysicObject:
        # TODO(n2one): Change to sprite object
        pass

    @staticmethod
    def _construct_sprite_type(color: str, position: list, size: list) -> PhysicObject:
        return Rectangle(
            position=Vector2(position),
            width=size[0],
            height=size[1],
            color=color
        )
