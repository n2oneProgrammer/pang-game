from models.graphics.scenes.scene import Scene
from models.map_builder import MapBuilder


class Map(Scene):
    def __init__(self):
        super().__init__()
        self.map_builder = MapBuilder("test_map.map")
        self.objects = self.map_builder.get_elements()
