#!/usr/bin/python

import sys, os
import numpy as np
from math import*


import matplotlib.pyplot as plt
import numpy as np


Fs = 8000
f = 5
sample = 8000
x = np.arange(sample)
y = np.sin(2 * np.pi * f * x / Fs)
plt.plot(x, y)
plt.xlabel('voltage(V)')
plt.ylabel('sample(n)')
plt.show()

