"""
datasets.py
-----------

Datasets for testing / analysis.
"""


import numpy as np
import pandas as pd


# Random dataset
def random_dataset(n_rows=100000, n_columns=2, null_proportion=0.25):
    """
    Generates a dataset full of random numbers between 0 and 1

    Parameters
    ----------
    n_rows : int
        Number of observations
    n_columns : int
        Number of features
    null_proportion : float
        Percent (per column) of observations that will be randomly converted to null values

    Returns
    -------
    pandas.DataFrame
        Random dataset
    """

    # Generate random data
    df = pd.DataFrame(np.random.rand(n_rows, n_columns))

    # Insert nulls?
    if null_proportion > 0.:
        # Number of nulls
        n_nulls = int(n_rows * null_proportion)

        # Nullify on a per column basis
        for j in range(n_columns):
            # Rows to nullify
            i = np.random.randint(low=0, high=n_rows, size=n_nulls)

            # Nullify
            df.iloc[i, j] = np.nan

    # Return
    return df
