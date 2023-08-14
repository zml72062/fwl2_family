from typing import Dict, Any, FrozenSet, Tuple, Iterable

class MultiSet:
    def __init__(self):
        self.contents: Dict[Any, int] = {}

    def add(self, obj: Any):
        if obj in self.contents:
            self.contents[obj] += 1
        else:
            self.contents[obj] = 1
    
    @staticmethod
    def from_iterable(s: Iterable) -> "MultiSet":
        multiset = MultiSet()
        for elem in s:
            multiset.add(elem)
        return multiset

    def __repr__(self) -> str:
        return repr(self.contents)
    
    def __eq__(self, other) -> bool:
        return isinstance(other, MultiSet) and self.contents == other.contents

class FrozenMultiSet:
    def __init__(self):
        self.contents: FrozenSet[Tuple[Any, int]]
    
    @staticmethod
    def from_multiset(s: MultiSet) -> "FrozenMultiSet":
        multiset = FrozenMultiSet()
        multiset.contents = frozenset(
            {(elem, cnt) for (elem, cnt) in s.contents.items()}
        )
        return multiset
    
    @staticmethod
    def from_iterable(s: Iterable) -> "FrozenMultiSet":
        return FrozenMultiSet.from_multiset(MultiSet.from_iterable(s))
    
    def __repr__(self) -> str:
        return repr({elem: cnt for (elem, cnt) in self.contents})
    
    def __eq__(self, other) -> bool:
        return isinstance(other, FrozenMultiSet) and self.contents == other.contents
    
    def __hash__(self) -> int:
        return hash(self.contents)
