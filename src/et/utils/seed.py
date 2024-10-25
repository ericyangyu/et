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

def set_env_seed(env: Env | List[Env], seed: int):
    """
    Set the gymnasium env seed
    """
    if isinstance(env, Env):
        env = [env]
    for _env in env:
        _env.reset(seed=seed)
        _env.action_space.seed(seed)
    logger.info(f"Fixed env seed to {seed}")

