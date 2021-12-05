from models.graphics.scenes.scene import Scene

from models.objects.sprite import Sprite


class Map(Scene):
    def __init__(self):
        super().__init__()
        self.objects.append(Sprite('bob.png', (50, 50), width = 150))
