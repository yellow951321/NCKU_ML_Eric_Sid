# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 07:51:02 2019

@author: huang
"""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

data = load_iris()

x = data.data
y = data.target