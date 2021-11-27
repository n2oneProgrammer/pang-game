class Scene:
    def __init__(self):
        self.objects = []

    def update(self):
        for obj in self.objects:
            from models.game_manager import GameManager
            obj.draw(GameManager().screen)
