import numpy as np
import scipy.optimize as sop


class ParabolaModel(object):
    """A parabolic model, mz ~ mz_idx^2."""

    def __init__(self):
        self.b = None

    def get_contingency_matrix(self, x):
        x = np.array(x)
        return np.stack([np.ones(x.shape), x, x**2], axis=1)

    def fit(self, x, y):
        """Fit a simple model y = a + b*x + c*x**2."""
        self.x = np.array(x)
        self.y = np.array(y)
        X = self.get_contingency_matrix(self.x)
        self.res = sop.lsq_linear(X, self.y)
        self.b = self.res['x']

    def __call__(self, x):
        """Predict values of new data points.

        Args:
            x (np.array): The control variable.
            *args       : Additional arguments.
            **kwds      : Additional arguments.

        Returns:
            np.array : Predicted values corresponding to values of 'x'.
        """
        x = np.array(x)
        assert self.b is not None, "Fit the model first."
        return self.b[0] + self.b[1]*x + self.b[2]*x**2

    def fitted(self):
        return self.__call__(self.x)

    def res(self):
        return self.y - self.fitted()

    def plot(self, show=True):
        import matplotlib.pyplot as plt
        plt.plot(self.x, self.fitted(), c='red')
        plt.scatter(self.x, self.y)
        if show:
            plt.show()