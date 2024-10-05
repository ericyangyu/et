import time

from loguru import logger
from wandb.sdk.wandb_run import Run


def setup_wandb_run(run: Run, postfix: str = None):
    """
    Set up the name of the run in wandb.
    The name will be in the format "mm.dd-hh:mm - run_id - postfix"

    Parameters
    ----------
    run: wandb.sdk.wandb_run.Run
        The run object from wandb.
    postfix: str
        The postfix to add to the run

    Returns
    -------
    None
    """
    # # Make sure that there are no slashes in the postfix
    # if postfix and "/" in postfix:
    #     raise ValueError(f"The postfix cannot contain any slashes: {postfix}")

    date = time.strftime("%m.%d-%H:%M")
    run_dir = name = f"{date}-{run.id}"
    if postfix:
        name += f" - {postfix}"
    run.name = name
    logger.info(f"Run name set to {name}")
    return 'runs/' + run_dir

