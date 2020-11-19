class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def action(self, percept):
        raise NotImplementedError()
