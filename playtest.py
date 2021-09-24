import numpy as np


from agents.custom_agent import CustomAgent
from envs.wrappers import addtimelimitwrapper_fn


from rollout import run_batched_rollout
from envs.batched_env import BatchedEnv


def evaluate():
    batched_env = BatchedEnv(env_make_fn=addtimelimitwrapper_fn, num_envs=1)

    agent = CustomAgent(1, batched_env.num_actions, verbose=True)

    ascensions, scores = run_batched_rollout(1, batched_env, agent)
    print(
        f"Ascensions: {ascensions} "
        f"Median Score: {np.median(scores)}, "
        f"Mean Score: {np.mean(scores)}"
    )
    return np.median(scores)


if __name__ == "__main__":
    evaluate()
