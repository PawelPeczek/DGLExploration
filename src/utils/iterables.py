from functools import reduce
from typing import TypeVar, Dict, Tuple, List, Iterable

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
