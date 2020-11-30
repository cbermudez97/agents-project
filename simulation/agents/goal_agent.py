from random import randint

from .robot import Robot
from ..environment.room import RoomEnv, FreeCell, DirtyCell, CorralCell, ObstacleCell
from ..environment.env_actions import *


# Goals
CLEAN, CHASE, STORE = range(3)

class Model:
    pass

class GoalRobot(Robot):
    def __init__(self, x, y):
        super(GoalRobot, self).__init__(x, y)
        self.model = Model()
        self.model.goal = None
        self.model.t = 0
        self.model.gt = 0

    def consider_goal(self, percept:RoomEnv):
        if self.model.t % percept.rt == percept.rt - 1: self.model.goal = None
        if self.model.gt >= percept.rt // 3: self.model.goal = None
        if not self.model.goal:
            if (percept.ndirty/(percept.ndirty + percept.free)) * 100 >= 30:
                return CLEAN
            if (percept.ndirty/(percept.ndirty + percept.free)) * 100 <= 20 \
                and not self.loading \
                and any([ percept.floor[k.x][k.y] != CorralCell for k in percept.kids ]):
                return CHASE
            elif self.loading:
                return STORE
            return CLEAN
        return self.model.goal

    def work_goal(self, percept:RoomEnv):
        if self.model.goal == CLEAN:
            if percept.floor[self.x][self.y] == DirtyCell:
                return Clean
            return self.find_nearest(percept, DirtyCell)
        elif self.model.goal == CHASE:
            if not self.loading:
                return self.find_nearest(percept, -1, baby=True)
            self.model.goal = None
            self.consider_goal(percept)
            return self.work_goal(percept)
        elif self.model.goal == STORE:
            if self.loading:
                if percept.floor[self.x][self.y] == CorralCell:
                    return DropKid
                return self.find_nearest(percept, CorralCell)
            self.model.goal = None
            self.consider_goal(percept)
            return self.work_goal(percept)
        return Hold

    def action(self, percept:RoomEnv):
        self.model.t += 1
        self.model.gt += 1
        self.model.goal = self.consider_goal(percept)
        return self.work_goal(percept)
