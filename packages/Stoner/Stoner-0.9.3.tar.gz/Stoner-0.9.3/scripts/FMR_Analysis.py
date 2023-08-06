#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 21:47:27 2019

@author: phygbu
"""


from Stoner import DataFolder
from Stoner.Fit import FMR_Power
import os
import numpy as np

directory = r"/sshfs/phygbu@stonerlab/storage/data/Projects/Organics/FMR/Satam/20191003/Second Time"
pattern = "*.txt"
x = "Field"
y = "FMR_Signal"


def sign(r):
    return np.sign(r.x)


os.chdir(directory)

fldr = DataFolder(directory, pattern=pattern, setas={"x": x, "y": y})
for d in fldr:
    fldr += d.split(sign, final="groups")
