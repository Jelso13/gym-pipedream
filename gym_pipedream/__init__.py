from gym.envs.registration import register

register(id="PipeDream-v0",
    entry_point="gym_pipedream.envs:PipeDreamEnv"
)