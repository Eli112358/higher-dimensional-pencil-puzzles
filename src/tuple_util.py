def ensure(t):
	if type(t) is int:
		return t, t
	if type(t) is str:
		return ensure(int(t))
	if type(t) is list:
		return tuple(t)
	if type(t) is not tuple:
		raise TypeError
	return t


def formula(t_a, t_b, t_c):
	return tuple((a * b) + c for a, b, c in zip(ensure(t_a), ensure(t_b), ensure(t_c)))
