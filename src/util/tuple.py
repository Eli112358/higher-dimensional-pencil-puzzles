from typing import (
	Callable,
	Union,
	Tuple,
	List,
	AnyStr,
	SupportsInt,
)

TupleAble = Union[
	AnyStr,
	List,
	SupportsInt,
	Tuple,
]


def ensure(t: TupleAble) -> Tuple:
	if type(t) is int:
		return t, t
	if type(t) is str:
		return ensure(int(t))
	if type(t) is list:
		return tuple(t)
	if type(t) is not tuple:
		raise TypeError
	return t


def formula(f: Callable, *ts: TupleAble) -> Tuple:
	return tuple(f(*a) for a in zip(*[ensure(t) for t in ts]))
