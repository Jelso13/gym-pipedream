from gym.envs.registration import register

def _register_env(id, **kwargs):
    register(
        id=id,
        entry_point='gym_pipedream.envs:PipeDreamEnv',
        kwargs=kwargs,
    )


#kwargs = {
#    render_mode:"ascii",
#    obs_mode:"default"
#}
#
#register(id="PipeDream-v0",
#    entry_point="gym_pipedream.envs:PipeDreamEnv",
#    kwargs=kwargs,
#)
#
#register(id="PipeDream-v1",
#    entry_point="gym_pipedream.envs:default_env",
#    kwargs=kwargs,
#)

_register_env("PipeDream-v0", render_mode="ascii", obs_mode="default")
_register_env("PipeDream-v1", render_mode="ascii", obs_mode="default")
