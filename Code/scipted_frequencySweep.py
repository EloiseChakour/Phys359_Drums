# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 15:07:56 2021

@author: elois
"""

import mcphysics
#import numpy as np


mcphysics.experiments.drum/list_com_ports()

a = mcphysics.instruments.adalm2000()

sc = mcphysics.instruments.soundcard()

#m = mcphysics.experiments.drum.motors_api('COM4', shape='circle')