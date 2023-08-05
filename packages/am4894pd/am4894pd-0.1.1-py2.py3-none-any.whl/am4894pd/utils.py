import pandas as pd
import numpy as np


def df_info(df: pd.DataFrame, return_info=False, shape=True, cols=True, info_prefix=''):
    """ Print a string to describe a df.
    """
    info = info_prefix
    if shape:
        info = f'{info}Shape = {df.shape}'
    if cols:
        info = f'{info} , Cols = {df.columns.tolist()}'
    print(info)
    if return_info:
        return info


def df_dummy_ts(start='2019-01-01', end='2019-01-02', freq='1s', n_cols=5):
    """ Make dummy ts df.
    """
    time_range = pd.DataFrame(pd.date_range(start, end, freq=freq), columns=['time'])
    data = pd.DataFrame(np.random.randn(len(time_range), n_cols), columns=[f'col{n}' for n in range(n_cols)])
    df = pd.concat([time_range, data], axis=1)
    return df


