from random import randint

from .robot import Robot
from ..environment.room import RoomEnv, FreeCell, DirtyCell, CorralCell, ObstacleCell
from ..environment.env_actions import *


class Model:
    pass

class ModelReflexRobot(Robot):
    def __init__(self, x, y):
        super(ModelReflexRobot, self).__init__(x, y)
        self.model = Model()
        self.model.visited = dict()
        self.model.t = 0

    def find_nearest(self, percept:RoomEnv, cell_type):
        queue = [(self.x, self.y, Hold)]
        visit = dict()
        visit[self.x, self.y] = True
        while queue:
            ax, ay, fac = queue.pop(0) 
            for it in [MovNorth, MovEast, MovSouth, MovWest]:
                mx = dx[it]
                my = dy[it]
                mov = (ax + mx, ay + my)
                ufac = fac
                if fac == Hold: ufac = it
                
                if not mov in visit \
                    and percept.valid_pos(*mov) \
                    and percept.floor[mov[0]][mov[1]] != ObstacleCell \
                    and not any([ a.x == mov[0] and a.y == mov[1] for a in percept.agents ]) \
                    and not (percept.floor[mov[0]][mov[1]] == CorralCell \
                        and any([k.x == mov[0] and k.y == mov[1] for k in percept.kids])):
                    if percept.floor[ax + mx][ay + my] == cell_type:
                        return ufac
                    visit[mov] = True
                    queue.append((*mov, ufac))
            if self.loading:
                # Check double moves
                for fit, batch in [(MovNorth, [MovNWest, MovNEast, MovNorth2]), 
                                    (MovEast, [MovNEast, MovSEast, MovEast2]), 
                                    (MovSouth, [MovSEast, MovSWest, MovSouth2]), 
                                    (MovWest, [MovSWest, MovNWest, MovWest])]:
                    fmx = dx[fit]
                    fmy = dy[fit]
                    fmov = (ax + fmx, ay + fmy)
                    if percept.valid_pos(*fmov) \
                        and percept.floor[fmov[0]][fmov[1]] != ObstacleCell \
                        and not any([ a.x == fmov[0] and a.y == fmov[1] for a in percept.agents ]) \
                        and not (percept.floor[fmov[0]][fmov[1]] == CorralCell \
                            and any([k.x == fmov[0] and k.y == fmov[1] for k in percept.kids])):
                        for it in batch:
                            mx = dx[it]
                            my = dy[it]
                            mov = (ax + mx, ay + my)
                            ufac = fac
                            if fac == Hold: ufac = it
                            if not mov in visit \
                                and percept.valid_pos(*mov) \
                                and percept.floor[mov[0]][mov[1]] != ObstacleCell \
                                and not any([ a.x == mov[0] and a.y == mov[1] for a in percept.agents ]) \
                                and not (percept.floor[mov[0]][mov[1]] == CorralCell \
                                    and any([k.x == mov[0] and k.y == mov[1] for k in percept.kids])):
                                if percept.floor[ax + mx][ay + my] == cell_type:
                                    return ufac
                                visit[mov] = True
                                queue.append((*mov, ufac))
        return Hold

    def go_to_corral(self, percept:RoomEnv):
        return self.find_nearest(percept, CorralCell)

    def move_around(self, percept:RoomEnv):
        t = None
        move = None
        for it in [MovNorth, MovEast, MovSouth, MovWest]:
            mx = dx[it]
            my = dy[it]
            mov = (self.x + mx, self.y + my)
            if percept.valid_pos(*mov) and percept.floor[mov[0]][mov[1]] != ObstacleCell and not any([ other.x == mov[0] and other.y == mov[1] for other in percept.agents ]):
                if not mov in self.model.visited:
                    self.model.visited[mov] = self.model.t
                    return it
                elif not move:
                    move = it
                    t = self.model.visited[mov]
                elif self.model.visited[mov] < t:
                    move = it
                    t = self.model.visited[mov]
        return randint(MovNorth, MovWest)

    def action(self, percept: RoomEnv):
        self.model.t += 1
        if self.model.t % percept.rt == 1: self.model.visited.clear()
        if self.loading:
            if percept.floor[self.x][self.y] == CorralCell: return DropKid
            return self.go_to_corral(percept)
        if percept.floor[self.x][self.y] == DirtyCell: return Clean
        if percept.floor[self.x][self.y] in [FreeCell, CorralCell]: return self.move_around(percept)
        return Hold
