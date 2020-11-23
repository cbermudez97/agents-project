from simulation.agents import KidAgent, HumanRobot, ModelReflexRobot
from simulation.environment import RoomEnv



def test_agent_model(agent_model, ntest=30, args=None, kwargs=None):
    victory = 0
    defeat  = 0
    tie     = 0
    uargs = (10, 10, 3, 1, 3, 3, agent_model, KidAgent)
    ukwargs = { 'rand_time':100 }
    if args: uargs = args
    if kwargs: ukwargs = kwargs
    for _ in range(ntest):
        room = RoomEnv(*uargs, **ukwargs)
        while True:
            total_free_cells = room.ndirty + room.free
            if (room.ndirty/total_free_cells) * 100 >= 40:
                defeat += 1
                break
            if room.is_clean():
                victory += 1
                break
            if room.t == room.rt * 100:
                tie += 1
                break
            room.step()
    print(f'Testing {agent_model.__name__}:')
    print(f'The robot has win in {victory} times.')
    print(f'The robot has lose in {defeat} times.')
    print(f'The simulations has end inconclusive in {tie} times.')

test_agent_model(ModelReflexRobot)
