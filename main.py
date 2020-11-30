from simulation.agents import KidAgent, HumanRobot, ModelReflexRobot, GoalRobot
from simulation.environment import RoomEnv


def test_agent_model(agent_model, ntest=30, args=None, kwargs=None):
    victory = 0
    defeat  = 0
    tie     = 0
    dirty = 0
    uargs = (10, 10, 3, 1, 3, 3, agent_model, KidAgent)
    ukwargs = { 'rand_time':10 }
    if args: uargs = args
    if kwargs: ukwargs = kwargs
    for _ in range(ntest):
        room = RoomEnv(*uargs, **ukwargs)
        while True:
            total_free_cells = room.ndirty + room.free
            if (room.ndirty/total_free_cells) * 100 >= 60:
                defeat += 1
                dirty += room.ndirty
                break
            if room.is_clean():
                victory += 1
                dirty += room.ndirty
                break
            if room.t == room.rt * 100:
                tie += 1
                dirty += room.ndirty
                break
            room.step()
    print(f'Testing {agent_model.__name__}:')
    print(f'\tTest params are:')
    print(f'\t\tSize:{uargs[0]}x{uargs[1]}')
    print(f'\t\tNumber of Babies:{uargs[2]}')
    print(f'\t\tNumber of Obst.:{uargs[4]}')
    print(f'\t\tInitial Dirty squares:{uargs[5]}')
    print(f'\t\tThe robot has win in {victory} times.')
    print(f'\t\tThe robot has lose in {defeat} times.')
    print(f'\t\tThe simulations has end inconclusive in {tie} times.')
    print(f'\t\tThe average amount of dirty cells is {dirty/ntest}')

def full_test_suite(model):
    envs = [
        ((5, 5, 2, 1, 3, 3, model, KidAgent), { 'rand_time':10 }),
        ((10, 10, 3, 1, 20, 15, model, KidAgent), { 'rand_time':9 }),
        ((15, 15, 3, 1, 30, 20, model, KidAgent), { 'rand_time':9 }),
        ((20, 20, 4, 1, 50, 35, model, KidAgent), { 'rand_time':10 }),
        ((10, 10, 3, 1, 10, 15, model, KidAgent), { 'rand_time':10 }),
        ((15, 15, 4, 1, 15, 20, model, KidAgent), { 'rand_time':10 }),
        ((20, 20, 5, 1, 25, 35, model, KidAgent), { 'rand_time':11 }),
        ((10, 10, 4, 1, 30, 15, model, KidAgent), { 'rand_time':13 }),
        ((15, 15, 5, 1, 45, 20, model, KidAgent), { 'rand_time':13 }),
        ((20, 20, 6, 1, 75, 35, model, KidAgent), { 'rand_time':14 }),
    ]
    for args, kwargs in envs:
        test_agent_model(model, args=args, kwargs=kwargs)

full_test_suite(ModelReflexRobot)
print()
full_test_suite(GoalRobot)


# room = RoomEnv(*(5, 5, 3, 1, 3, 3, GoalRobot, KidAgent), **{ 'rand_time':10 })
# while True:
#     print(room)
#     input('Continue...')
#     room.step()
