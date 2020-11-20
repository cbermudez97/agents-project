from random import randint, random

from ..agents import Robot
from .env_actions import *


# Env Floor Cells
FreeCell, DirtyCell, CorralCell, ObstacleCell = range(4)

# Env class
class RoomEnv:
    def __init__(self, rows, columns, nkids, nagents, nobstacles, ndirt, agent_model, baby_model, kid_mess_prob=0.4, rand_time=1000):
        self.floor = [ [FreeCell]*columns for _ in range(rows) ]
        self.kid_mess_prob = kid_mess_prob
        self.t = 0
        self.rt = rand_time
        self.kids = []
        self.agents = []

        # Statistics

        # Add CorralCell
        x, y = 0, 0
        while True:
            x, y = (randint(0, rows-1), randint(0, columns-1))
            if self.floor[x][y] != FreeCell:
                continue
            self.floor[x][y] = CorralCell
            break
        self.build_corral(x, y, nkids-1)
        
        # Add DirtyCells
        for _ in range(ndirt):
            while True:
                x, y = (randint(0, rows-1), randint(0, columns-1))
                if self.floor[x][y] != FreeCell:
                    continue
                self.floor[x][y] = DirtyCell
                break

        # Add ObstacleCell
        for _ in range(nobstacles):
            while True:
                x, y = (randint(0, rows-1), randint(0, columns-1))
                if self.floor[x][y] != FreeCell:
                    continue
                self.floor[x][y] = ObstacleCell
                break

        # Add Kids
        for _ in range(nkids):
            while True:
                x, y = (randint(0, rows-1), randint(0, columns-1))
                if self.floor[x][y] != FreeCell or self.occupy(x, y):
                    continue
                self.kids.append(baby_model(x, y))
                break
        
        # Add agents
        for _ in range(nagents):
            while True:
                x, y = (randint(0, rows-1), randint(0, columns-1))
                if self.floor[x][y] != FreeCell or self.occupy(x, y) :
                    continue
                self.agents.append(agent_model(x, y))
                break    
    
    def build_corral(self, x, y, size):
        corral = [(x,y)]
        while True:
            ax, ay = corral.pop(0)
            for mx, my in zip(dx, dy):
                if not size:
                    return
                if self.free_cell(ax + mx, ay + my):
                    self.floor[ax + mx][ay + my] = CorralCell
                    corral.append((ax+mx, ay+my))
                    size -= 1

    def step(self):
        for agent in self.agents:
            self.aply_agent_action(agent, agent.action(self))
        for kid in self.kids:
            self.aply_kid_action(kid, kid.action(self))
        if self.t % self.rt: self.randomize()
        self.t += 1

    def randomize(self):
        pass

    def aply_kid_action(self, kid, action):
        if not action in [ MovNorth, MovSouth, MovWest, MovEast, Hold]:
            raise ValueError('Invalid action to be aplied by kid.')
        if action == Hold or kid.loaded():
            return
        mx, my = dx[action], dy[action]
        if self.kid_push(kid.x + mx, kid.y + my, mx, my):
            tmx = kid.x
            tmy = kid.y
            kid.x = tmx + mx
            kid.y = tmy + my
            self.kid_mess(tmx, tmy)
            
    def kid_mess(self, x, y):
        mess = random()
        if mess > self.kid_mess_prob:
            return
        kids_around = [ kid for kid in self.kids if abs(x-kid.x) < 2 and abs(y-kid.y) < 2]
        to_mess = 9 - len(kids_around)
        if len(kids_around) == 1: to_mess = 1
        if len(kids_around) == 2: to_mess = 3
        cedx = list(edx)
        cedy = list(edy)
        while to_mess and cedx:
            pos = randint(0,len(cedx)-1)
            mx, my = cedx.pop(pos), cedy.pop(pos)
            if self.free_cell(x + mx, y + my) and not self.occupy(x + mx, y + my):
                self.floor[x][y] = DirtyCell
                to_mess -= 1

    def kid_push(self, x, y, mx, my):
        if not self.valid_pos(x, y):
            return False
        if self.floor[x][y] == FreeCell and not self.occupy(x, y):
            return True
        elif self.floor[x][y] == ObstacleCell:
            if self.kid_push(x+mx, y+my, mx, my):
                self.floor[x][y] = FreeCell
                self.floor[x+mx][y+my] = ObstacleCell
                return True
        return False

    def aply_agent_action(self, agent, action):
        if action >= DropKid and not agent.loading:
            raise ValueError('Invalid action to be aplied by agent.')
        mx = edx[action]
        my = edx[action]
        ax = agent.x
        ay = agent.y
        if action == Hold:
            return
        elif action == Clean:
            if self.floor[ax][ay] == DirtyCell:
                self.floor[ax][ay] = FreeCell
                return
        elif action == DropKid:
            agent.loading.loaded_by = None
            agent.loading = None
        elif self.valid_pos(ax + mx, ay + my) and self.floor[ax + mx][ay + my] != ObstacleCell and not any([ other.x == ax + mx and other.y == ay + my for other in self.agents ]):
            if not self.occupy(ax + mx, ay + my):
                agent.x += mx
                agent.y += my
                agent.loading.x += mx
                agent.loading.y += my
            elif not agent.loading:
                kid = [ kid for kid in self.kids if kid.x == ax + mx and kid.y == ay + my ][0]
                agent.loading = kid
                kid.loaded_by = agent
                agent.x += mx
                agent.y += my

    def valid_pos(self, x, y):
        return x >= 0 and x < len(self.floor) and y >= 0 and y < len(self.floor[0])
    
    def occupy(self, x, y):
        return any(agent.x == x and agent.y == y for agent in self.agents + self.kids) 

    def free_cell(self, x, y):
        return self.valid_pos(x, y) and self.floor[x][x] == FreeCell

    def __str__(self):
        result = ''
        # legend = 'Free     - .\nCorral   - C\nDirty    - D\nObstacle - X\nBaby     - B\nRobot    - R'
        for i in range(len(self.floor)):
            for j in range(len(self.floor[0])):
                cell = ''
                if self.floor[i][j] == FreeCell: cell = '. '
                if self.floor[i][j] == CorralCell: cell = 'C '
                if self.floor[i][j] == DirtyCell: cell = 'D '
                if self.floor[i][j] == ObstacleCell: cell = 'X '
                if any([ kid.x == i and kid.y == j for kid in self.kids ]): cell = 'B '
                if any([ agent.x == i and agent.y == j for agent in self.agents ]): cell = 'R '
                result += cell
            result += '\n'
        # result += legend
        return result
