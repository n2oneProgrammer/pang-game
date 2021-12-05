from models.graphics.scenes.scene import Scene

from models.objects.sprite import Sprite


class Map(Scene):
    def __init__(self):
        super().__init__()
        self.objects.append(Sprite('bob.png', (0, 100), 90, 150, 90, 40))
