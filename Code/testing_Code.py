# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 14:21:24 2021

@author: elois
"""

import spinmob
import mcphysics



a = mcphysics.instruments.adalm2000()

sc = mcphysics.instruments.soundcard()

m = mcphysics.experiments.drum.motors_api('COM4', shape='circle')

