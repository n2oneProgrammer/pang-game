from models.graphics.scenes.scene import Scene

from models.objects.rectangle import Rectangle


class Map(Scene):
    def __init__(self):
        self.objects = []
        self.objects.append(Rectangle((0, 100), 90, 40))

    def update(self):
        for obj in self.objects:
            from models.game_manager import GameManager
            obj.draw(GameManager().screen)
