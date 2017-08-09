# Utilies: includes ODE solver, plotting functions, data generator, green glob intersection

def time_piece(globs, tmax=100):
	min_d   = min(2*glob.radius for glob in globs)
	i       = 0
	tp_dict = {0:[]}
	while i+min_d < tmax:
		i += min_d
		tp_dict[i] = []
	for i in xrange(len(globs)):
		min_j = float('+inf')
		for j in tp_dict:
			if abs(min_j-globs[i].x) < abs(j-globs[i].x):
				min_j = j
		tp_dict[min_j].append(i)
	return tp_dict
