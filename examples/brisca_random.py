import rlcard
from rlcard.agents import RandomAgent

env = rlcard.make('brisca', config={'allow_step_back': False, 'allow_raw_data': False})
episode_num = 100
p1_total_reward = 0
agent_0 = RandomAgent(action_num=env.action_num)
agent_1 = RandomAgent(action_num=env.action_num)
env.set_agents([agent_0, agent_1])

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _ = env.run(is_training=False)

    # Print out the trajectories
    print('\nEpisode {}'.format(episode))
    for ts in trajectories[0]:
        if ts[4]:
            p1_total_reward += ts[2]
        print('State: {}, Action: {}, Reward: {}, Next State: {}, Done: {}'.format(ts[0], ts[1], ts[2], ts[3], ts[4]))

print()
print('Player 1 reward:', p1_total_reward)
