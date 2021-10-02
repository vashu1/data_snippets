"""
linear regressio
"""

import numpy as np
from sklearn.linear_model import LinearRegression

x = np.array([0,1,2,3,4,5]).reshape((-1, 1))
y = np.array([25, 36, 45, 54, 72, 83])

model = LinearRegression()

model.fit(x, y)

model.predict(np.array([6]).reshape((-1, 1)))