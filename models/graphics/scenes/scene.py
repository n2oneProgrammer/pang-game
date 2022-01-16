class Scene:
    def __init__(self):
        self.objects = []
        self.bullets = []

    def update(self, delta_time):

        from models.game_manager import GameManager
        screen = GameManager().screen
        for bullet in self.bullets:
            bullet.draw(screen)

        for obj in self.objects:
            obj.draw(screen)
