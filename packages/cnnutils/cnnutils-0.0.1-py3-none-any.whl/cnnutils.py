import numpy as np
def sigmoid(Z):
	#Sigmoid activation function
	A = 1/(1+np.exp(-Z))
	cache = Z
	return A, cache

print(sigmoid(5))
