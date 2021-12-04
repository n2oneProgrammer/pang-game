import os


class MapBuilder:
    def __init__(self, src_map):
        self.src_map = src_map
        self.assets = []

    def get_elements(self):
        pass

    def load_assets(self):
        pass

    def construct_object(self, object_json):
        pass
    
    def construct_asset(self, asset_json):
        if "name" not in asset_json or type(asset_json["name"]) is not str:
            raise ValueError("Assert object must have name")
        if "src" not in asset_json or type(asset_json["src"]) is not str:
            raise ValueError("Assert object must have src (path to image)")

        asset_json["src"] = os.path.join("assets", asset_json["src"])
        if not os.path.exists(asset_json["src"]):
            raise FileNotFoundError(f"I cant find {asset_json['src']}")
        return asset_json

    def get_background(self):
        pass
