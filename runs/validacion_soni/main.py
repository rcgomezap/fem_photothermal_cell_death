# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 09:56:34 2024

@author: Melany Martinez
"""
import numpy as np

import sys
sys.path.append('../../')
from FEM.bridge.run_fenicsx import run_simultation

run_simultation()
T = np.load("T.npy")
print(T.max())