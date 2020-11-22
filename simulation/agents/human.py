from .robot import Robot
from ..environment.room import FreeCell, ObstacleCell
from ..environment.env_actions import *

class HumanRobot(Robot):
    def __init__(self, x, y):
        super(HumanRobot, self).__init__(x, y)
    
    def action(self, percept):
        op = input('Option:')
        return int(op)
        