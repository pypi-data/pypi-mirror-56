'''
Demos the function lm(), saved in linearmodel.py.
'''
# Demo of function.
import numpy as np
import pandas as pd

from patsy import demo_data   
data = pd.DataFrame(demo_data("a", "b", "x1", "x2", "y", "z column"))
data.head()
np.shape(data)

# Set train and test sets.
df_train = data; df_test = data

# Fit model.
mylm = lm("y ~ x1 + x2 + x1:x2", df_train, df_test)

# output is a dictionary.
mylm.keys()
len(mylm)

mylm['beta']
mylm['formula']

