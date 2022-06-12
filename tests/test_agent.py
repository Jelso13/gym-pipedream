import gym
import gym_pipedream

def test_random_agent(episodes=100):
    env = gym.make("PipeDream-v0")
    env.reset()
    env.render()
    for e in range(episodes):
        action = env.action_space.sample()
        print("action = ", action)
        state, reward, done, info = env.step(action)
        env.render()
        print(reward)
        if done:
            break

if __name__=="__main__":
    test_random_agent()
    test_random_agent(400)