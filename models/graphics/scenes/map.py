from models.graphics.scenes.scene import Scene

from models.objects.rectangle import Rectangle


class Map(Scene):
    def __init__(self):
        super().__init__()
        self.objects.append(Rectangle((0, 100), 90, 40))
