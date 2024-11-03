import numpy as np
import random
import os

from jax import Array
from loguru import logger
from typing import List, Union, Tuple, Iterable
from gymnasium import Env


def set_seed(seed: int = 0, use_torch: bool = False, use_jax: bool = False) -> Array:
    """
    https://wandb.ai/sauravmaheshkar/RSNA-MICCAI/reports/How-to-Set-Random-Seeds-in-PyTorch-and-Tensorflow--VmlldzoxMDA2MDQy
    """
    logger.info(f"Fixing seed to {seed}")
    np.random.seed(seed)
    random.seed(seed)
    # Set a_cands fixed value for the hash seed
    os.environ["PYTHONHASHSEED"] = str(seed)
    if use_torch:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        # When running on the CuDNN backend, two further options must be set
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    if use_jax:
        import jax.random as jr
        return jr.key(seed)

def set_env_seed(envs: Env | List[Env], seeds: int | List[int]) -> Env | List[Env]:
    """
    Set the gymnasium env seed
    """
    # Perform assertions for convenience's sake
    if isinstance(envs, List):
        assert isinstance(seeds, List), "Seeds must be a list if envs is a list"
        assert len(envs) == len(seeds), f"Number of seeds {len(seeds)} must match number of envs {len(envs)}"
        num_envs = len(envs)
    else:
        assert isinstance(envs, Env), "Env must be a gymnasium.Env instance"
        assert isinstance(seeds, int), "Seeds must be an integer if envs is a single env"
        envs, seeds = [envs], [seeds]
        num_envs = 1

    for env, seed in zip(envs, seeds):
        env.reset(seed=seed)
        env.action_space.seed(seed)
    logger.info(f"Seeded envs to {seeds}")
    return envs if num_envs > 1 else envs[0]

