# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 09:56:34 2024

@author: Melany Martinez
"""
import sys
import os
dir = os.path.dirname(os.path.realpath(__file__))
dir1 = os.path.abspath('../..')
sys.path.append(dir1)

import numpy as np
from FEM.bridge.run_fenicsx import run_simultation

# run_simultation(dir)
T = np.load("T.npy")
print(T.max())