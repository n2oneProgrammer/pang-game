import time


class Animation:
    def __init__(self, sprite, sources, change_time):
        self.sprite = sprite
        self.sources = sources
        self.state = 0
        self.change_time = change_time
        self.last_change = time.time()
        self.is_enabled = True

    def update(self):
        if self.is_enabled and time.time() - self.last_change > self.change_time:
            self.last_change = time.time()
            self.state = (self.state + 1) % len(self.sources)
            self.sprite.change_img_src(self.sources[self.state])

    def change_enabled(self, value):
        if self.is_enabled != value:
            self.last_change = time.time() - self.change_time
            self.update()
        self.is_enabled = value
