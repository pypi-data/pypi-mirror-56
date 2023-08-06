from gym.envs.registration import register

register(
    id='bci-v0',
    entry_point='gym_bci.envs:BCIEnv',
)
