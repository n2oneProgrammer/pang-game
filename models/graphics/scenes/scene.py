class Scene:
    def __init__(self):
        self.objects = []

    def update(self, delta_time):
        for obj in self.objects:
            from models.game_manager import GameManager
            obj.draw(GameManager().screen)
