from __future__ import annotations
import random
from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple, List, Dict, Optional

CompactPosition2D = Tuple[int, int]


class Direction(Enum):
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

    def tu_tuple(self) -> CompactPosition2D:
        return self.x, self.y

    def __eq__(self, other: Any) -> bool:
        if type(other) != Position2D:
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return (self.x, self.y).__hash__()


@dataclass(frozen=True)
class FreeVector2D:
    x: int
    y: int


@dataclass(frozen=True)
class Person:
    person_id: int
    sick: bool
    position: Position2D
    sick_start: Optional[int] = None

    def get_move_vector(self, max_step_size: int) -> FreeVector2D:
        direction = random.choice(list(Direction))
        ox_step_size = random.randint(1, max_step_size)
        oy_step_size = random.randint(1, max_step_size)
        return FreeVector2D(
            x=direction.value[0] * ox_step_size,
            y=direction.value[1] * oy_step_size,
        )

    def update_position(self, new_position: Position2D) -> Person:
        return Person(
            person_id=self.person_id,
            sick=self.sick,
            position=new_position,
            sick_start=self.sick_start
        )

    def make_sick(self, time_stamp: int) -> Person:
        return Person(
            person_id=self.person_id,
            sick=True,
            position=self.position,
            sick_start=time_stamp
        )

    def __eq__(self, other: Any) -> bool:
        if type(other) != Person:
            return False
        return self.person_id == other.person_id

    def __hash__(self) -> int:
        return self.person_id.__hash__()


@dataclass(frozen=True)
class Contact:
    person_x: Person
    person_y: Person
    intensity: float
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
                          move_vector: FreeVector2D
                          ) -> Position2D:
        target_x = min(self.max_x, max(0, source_position.x + move_vector.x))
        target_y = min(self.max_y, max(0, source_position.y + move_vector.y))
        return Position2D(x=target_x, y=target_y)


@dataclass(frozen=True)
class SimulationState:
    map: Map
    people: List[Person]
    meetings: List[Contact]
    people_traces: Dict[Person, List[Position2D]]
