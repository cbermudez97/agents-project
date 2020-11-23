from simulation.agents import KidAgent, HumanRobot, ModelReflexRobot
from simulation.environment import RoomEnv



def test_agent_model(agent_model, ntest=30):
    victory = 0
    defeat  = 0
    tie     = 0
    for _ in range(ntest):
        room = RoomEnv(10, 10, 3, 1, 3, 3, agent_model, KidAgent, rand_time=100)
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
    return victory, defeat, tie

v, d, t = test_agent_model(ModelReflexRobot)
print(f'El robot a ganado en {v} ocasiones.')
print(f'El robot a perdido en {d} ocasiones.')
print(f'La simulacion a terminado inconclusa en {t} ocasiones.')
