# Env Actions
MovNorth, MovEast, MovSouth, MovWest, Hold, Clean, DropKid, MovSEast, MovNWest, MovNEast, MovSWest, MovNorth2, MovEast2, MovSouth2, MovWest2 = range(15)

# Directions
dx = [-1, 0, 1,  0, 0, 0, 0, 0]
dy = [ 0, 1, 0, -1, 0, 0, 0, 0]
edx = dx + [1, -1, -1,  1, -2, 0, 2,  0]
edy = dy + [1, -1,  1, -1,  0, 2, 0, -2]
