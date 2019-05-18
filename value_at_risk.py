# Python packages
import numpy as np
import pandas as pd
import math

def value_at_risk(data):
	# VaR level
	VaR_level = 0.99
	sample_size = len(data)
	
	# floor level index
	VaR_index = math.floor(sample_size*(1 - VaR_level))
	VaR = []
	# create VaR list
	for x in data.columns.values:
		temp = data[x].sort_values(axis=0, ascending=True)
		VaR.append(temp[VaR_index-1:VaR_index])

	# 'numpy.matrixlib.defmatrix.matrix (1,n)
	#VaR = np.matrix(VaR)
	return VaR
