import numpy as np
import scipy.optimize as optimization


def func(params, xdata, ydata):
    return (ydata - np.dot(xdata, params))


xdata = np.transpose(
    np.array(
        [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]]
    )
)
x0 = np.array([0.0, 0.0])

print(optimization.leastsq(func, x0, args=(xdata, ydata)))
