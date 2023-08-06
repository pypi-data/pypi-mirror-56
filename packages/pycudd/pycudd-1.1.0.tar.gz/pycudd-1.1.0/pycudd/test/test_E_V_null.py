import pycudd
mgr = pycudd.DdManager()
mgr.SetDefault()
pycudd.set_iter_meth(1) # nodes
func = mgr.IthVar(1) & mgr.IthVar(2)
nodes = [x for x in func]
print('nodes: ', nodes)
Enodes = [x.E() for x in func]
Tnodes = [x.T() for x in func]
