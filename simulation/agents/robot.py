from .agent import Agent
from ..environment.room import RoomEnv, FreeCell, DirtyCell, CorralCell, ObstacleCell
from ..environment.env_actions import *


class Robot(Agent):
    def __init__(self, x, y):
        super(Robot, self).__init__(x, y)
        self.loading = None

    def find_nearest(self, percept:RoomEnv, cell_type, baby=False, agent=False):
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
                    if percept.floor[ax + mx][ay + my] == cell_type \
                        or (baby and any([k.x == mov[0] and k.y == mov[1] for k in percept.kids])) \
                        or (agent and any([k.x == mov[0] and k.y == mov[1] for k in percept.agents])):
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
                                if percept.floor[ax + mx][ay + my] == cell_type \
                                    or (baby and any([k.x == mov[0] and k.y == mov[1] for k in percept.kids])) \
                                    or (agent and any([k.x == mov[0] and k.y == mov[1] for k in percept.agents])):
                                    return ufac
                                visit[mov] = True
                                queue.append((*mov, ufac))
        return Hold
