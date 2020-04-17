from __future__ import annotations
import random
from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple, List


class Move(Enum):
    STAY = (0, 0)
    NORTH = (0, -1)
    NORTH_EAST = (1, -1)
    EAST = (1, 0)
    SOUTH_EAST = (1, 1)
    SOUTH = (0, 1)
    SOUTH_WEST = (-1, 1)
    WEST = (-1, 0)
    NORTH_WEST = (-1, -1)


@dataclass(frozen=True)
class Position2D:
    x: int
    y: int

    def __eq__(self, other: Any) -> bool:
        if type(other) != Position2D:
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return (self.x, self.y).__hash__()


@dataclass(frozen=True)
class Person:
    person_id: int
    sick: bool
    position: Position2D

    def get_move_direction(self) -> Move:
        return random.choice(list(Move))

    def update_position(self, new_position: Position2D) -> Person:
        return Person(
            person_id=self.person_id,
            sick=self.sick,
            position=new_position
        )

    def make_sick(self) -> Person:
        return Person(
            person_id=self.person_id,
            sick=True,
            position=self.position
        )


@dataclass(frozen=True)
class Meeting:
    person_x: Person
    person_y: Person
    duration: float
    time_stamp: int

    def virus_transmission_can_occur(self) -> bool:
        return self.person_x.sick or self.person_y.sick

    def get_pair(self) -> Tuple[Person, Person]:
        return self.person_x, self.person_y

    def get_pair_ids(self) -> Tuple[int, int]:
        return self.person_x.person_id, self.person_y.person_id


@dataclass(frozen=True)
class Map:
    max_x: int
    max_y: int

    def get_next_position(self,
                          source_position: Position2D,
                          move: Move
                          ) -> Position2D:
        target_x = min(self.max_x, max(0, source_position.x + move.value[0]))
        target_y = min(self.max_y, max(0, source_position.x + move.value[1]))
        return Position2D(x=target_x, y=target_y)


@dataclass(frozen=True)
class SimulationState:
    people: List[Person]
    meetings: List[Meeting]
