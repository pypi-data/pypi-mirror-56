import pycudd
mgr = pycudd.DdManager()
mgr.SetDefault()

X = {}
for i in range(10):
	X[i] = mgr.IthVar(i)

f = (X[0] & X[1]) | X[2]
g = X[1] | X[0] & X[2]

h = f + g
