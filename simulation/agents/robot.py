from .agent import Agent


class Robot(Agent):
    def __init__(self, x, y):
        super(Robot, self).__init__(x, y)
        self.loading = None
