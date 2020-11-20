from random import randint

from .agent import Agent
from ..environment.room import FreeCell, ObstacleCell, CorralCell
from ..environment.env_actions import MovNorth, MovEast, MovSouth, MovWest, Hold, dx, dy


class KidAgent(Agent):
    def __init__(self, x, y):
        super(KidAgent, self).__init__(x,y)
        self.loaded_by = None

    def loaded(self):
        return not self.loaded_by is None
    
    def  action(self, percept):
        if percept.floor[self.x][self.y] == CorralCell or self.loaded_by: return Hold
        free = [ dir for dir in [MovNorth, MovEast, MovSouth, MovWest]                           \
            if percept.valid_pos(self.x + dx[dir], self.y + dy[dir])                             \
                and not percept.occupy(self.x + dx[dir], self.y + dy[dir])                       \
                and percept.floor[self.x + dx[dir]][self.y + dy[dir]] in [FreeCell, ObstacleCell]]
        free.append(Hold)
        op = randint(0, len(free)-1)
        return free[op]
