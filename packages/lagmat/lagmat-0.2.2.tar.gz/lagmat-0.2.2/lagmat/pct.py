
from .lagmat_func import lagmat
from .chopnan import chopnan
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import warnings


warnings.warn(
    ("'val_to_pct', 'pct_to_val', 'Pct' are deprecated and"
     "will be moved to 'pctreturn' and 'pctreturn-sklearn' packages."),
    DeprecationWarning, stacklevel=2)


def val_to_pct(val: np.array) -> np.array:
    """Convert values (e.g. prices) to percentage changes, discrete returns

    Parameters:
    -----------
    x : ndarray (2D)
        Time series with the oldest observation in the first row
        and the latest observation in the last row.
        Values need to be ratio-scale, i.e. x>0

    Returns:
    --------
    ret : ndarray (2D)
        percentage changes, discrete returns.
        The first row will be nan, i.e. r[0,;]=np.nan

    Alternative:
    ------------
        def val_to_pct(val):
            y = np.empty(shape=x.shape)
            y[0, :] = np.nan
            y[1:, :] = x[1:, :] / x[:-1, :] - 1
            return y
    """
    return val / lagmat(val, lags=[1]) - 1.0


def pct_to_val(ret: np.array, initial: float = 1.0) -> np.array:
    """Convert percentage changes, discrete returns into values or prices

    Returns:
    --------
    ret : ndarray (2D)
        percentage changes, discrete returns.

    initial: int or list/tupel/array
        Start values to compound the growth rates from

    Returns:
    --------
    x : ndarray (2D)
        Time series with the oldest observation in the first row
        and the latest observation in the last row.
    """
    z = 1.0 + ret
    z[0, :] = initial
    return np.cumprod(z, axis=0)


class Pct(BaseEstimator, TransformerMixin):
    def __init__(self, initial: float = None, trimnan: bool = True):
        self.initial = initial
        self.trimnan = trimnan

    def fit(self, X: np.array, y=None):
        # store the starting values
        if self.initial is None:
            if len(X.shape) == 1:
                self.initial = X[0]
            else:
                self.initial = X[0, :]
        # done
        return self

    def transform(self, X: np.array, copy=None) -> np.array:
        if self.trimnan:
            return chopnan(val_to_pct(X), nchop=1)
        else:
            return val_to_pct(X)

    def inverse_transform(self, Z: np.array, initial: float = None,
                          copy=None) -> np.array:
        # Use the requested initial value, or use the fitted initial values
        if initial is None:
            initial = self.initial
        # Multiply initial values repeatly by (1 + ret)
        if self.trimnan:
            return pct_to_val(
                np.r_[np.zeros(shape=(1, Z.shape[1])), Z],
                initial=initial)
        else:
            return pct_to_val(Z, initial=initial)
