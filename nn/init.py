import jax
import jax.numpy as jnp


def xavier_init(key: jax.random.PRNGKey, n_in: int, n_out: int, xavier_type: str = 'normal'):
    """
    Xavier initialization for weights.

    Parameters
    ----------
    key : PRNGKey
        Random key.
    n_in : int
        Number of input units.
    n_out : int
        Number of output units.
    xavier_type : str
        Type of Xavier initialization. Can be 'normal' or 'uniform'.
    """
    numer = 2 if xavier_type == 'normal' else 6  # 2 for normal, 6 for uniform
    return jax.random.normal(key, (n_in, n_out)) * jnp.sqrt(numer / (n_in + n_out))
