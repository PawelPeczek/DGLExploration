from functools import reduce
from typing import TypeVar, Dict, Tuple, List, Iterable
from itertools import islice

K = TypeVar("K")
V = TypeVar("V")


def create_dictionary_of_lists(dictionary_specs: List[Tuple[K, V]]
                               ) -> Dict[K, List[V]]:
    return reduce(append_to_dictionary_of_lists, dictionary_specs, {})


def append_to_dictionary_of_lists(dictionary: Dict[K, List[V]],
                                  to_append: Tuple[K, V]
                                  ) -> Dict[K, List[V]]:
    key, value = to_append
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]
    return dictionary


def flatten(to_flatten: Iterable[Iterable[V]]) -> List[V]:
    return [v for nested_list in to_flatten for v in nested_list]


def unzip_list(to_unzip: List[Tuple[V, V]]) -> Tuple[List[V], List[V]]:
    return list(zip(*to_unzip))


def sliding_window(seq: Iterable[V], n: int = 2) -> Iterable[Tuple[V, ...]]:
    """Returns a sliding window (of width n) over data from the iterable
       s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
    Source: https://stackoverflow.com/questions/6822725/rolling-or-sliding-window-iterator
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result
