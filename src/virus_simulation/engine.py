import itertools
import logging
import random
from copy import deepcopy
from typing import List, Dict

from src.utils.iterables import create_dictionary_of_lists, flatten
from src.virus_simulation.primitives import Map, Person, Position2D, Contact, \
    SimulationState
import src.config as global_config


logging.getLogger().setLevel(global_config.LOGGING_LEVEL)


PeopleGroup = List[Person]
OccupancyMap = Dict[Position2D, PeopleGroup]


class SimulationEngine:

    @classmethod
    def initialize(cls,
                   map_size: int,
                   max_person_step_size: int,
                   people_number: int,
                   initial_seek_people: int,
                   transmission_probability: float):
        simulation_map = Map(
            max_x=map_size,
            max_y=map_size
        )
        people = PeopleInitializer.initialize_people(
            simulation_map=simulation_map,
            people_number=people_number,
            initial_seek_people=initial_seek_people
        )
        return cls(
            simulation_map=simulation_map,
            people=people,
            transmission_probability=transmission_probability,
            max_person_step_size=max_person_step_size
        )

    def __init__(self,
                 simulation_map: Map,
                 people: List[Person],
                 transmission_probability: float,
                 max_person_step_size: int
                 ):
        self.__simulation_map = simulation_map
        self.__people = people
        self.__transmission_probability = transmission_probability
        self.__max_person_step_size = max_person_step_size
        self.__time_stamp: int = -1
        self.__meetings: List[Contact] = []
        self.__people_traces = {p: [] for p in people}

    def take_simulation_step(self) -> None:
        self.__time_stamp += 1
        self.__update_people_positions()
        occupancy_map = self.__calculate_occupancy_map()
        current_step_meetings = self.__generate_meetings_in_current_step(
            occupancy_map=occupancy_map
        )
        self.__update_people_health_status(
            current_step_meetings=current_step_meetings
        )
        self.__meetings.extend(current_step_meetings)

    def get_simulation_state(self) -> SimulationState:
        return SimulationState(
            map=deepcopy(self.__simulation_map),
            people=deepcopy(self.__people),
            meetings=deepcopy(self.__meetings),
            people_traces=deepcopy(self.__people_traces)
        )

    def __update_people_positions(self) -> None:
        people_after_move = []
        for person in self.__people:
            new_position = self.__generate_new_person_position(person=person)
            updated_person = person.update_position(new_position=new_position)
            people_after_move.append(updated_person)
            self.__people_traces[person].append(updated_person.position)
        self.__people = people_after_move

    def __generate_new_person_position(self, person: Person) -> Position2D:
        move_vector = person.get_move_vector(
            max_step_size=self.__max_person_step_size
        )
        return self.__simulation_map.get_next_position(
            source_position=person.position,
            move_vector=move_vector
        )

    def __calculate_occupancy_map(self) -> OccupancyMap:
        occupancy_map_specs = [
            (person.position, person) for person in self.__people
        ]
        return create_dictionary_of_lists(dictionary_specs=occupancy_map_specs)

    def __generate_meetings_in_current_step(self,
                                            occupancy_map: OccupancyMap
                                            ) -> List[Contact]:
        return flatten([
            self.__generate_meetings_inside_group(people_group)
            for people_group in occupancy_map.values()
        ])

    def __generate_meetings_inside_group(self,
                                         people_group: PeopleGroup
                                         ) -> List[Contact]:
        return [
            Contact(
                person_x=person_x,
                person_y=person_y,
                intensity=random.random(),
                time_stamp=self.__time_stamp
            ) for person_x, person_y in itertools.combinations(people_group, 2)
        ]

    def __update_people_health_status(self,
                                      current_step_meetings: List[Contact]
                                      ):
        people_before_transmission = {
            person.person_id: person for person in self.__people
        }
        transmission_endangered_meetings = [
            meeting for meeting in current_step_meetings
            if meeting.virus_transmission_can_occur()
        ]
        meetings_with_actual_transmission = [
            meeting for meeting in transmission_endangered_meetings
            if random.random() < meeting.intensity * self.__transmission_probability
        ]
        people_recently_infected = flatten(
            meeting.get_pair() for meeting in meetings_with_actual_transmission
        )
        people_recently_infected = {
            person.person_id: person.make_sick(time_stamp=self.__time_stamp)
            for person in people_recently_infected
            if person.sick is False
        }
        if len(people_recently_infected) > 0:
            logging.info(
                f"People recently infected: {len(people_recently_infected)}"
            )
        people_before_transmission.update(people_recently_infected)
        self.__people = list(people_before_transmission.values())


class PeopleInitializer:

    @staticmethod
    def initialize_people(simulation_map: Map,
                          people_number: int,
                          initial_seek_people: int
                          ) -> List[Person]:
        people_indices = [i for i in range(people_number)]
        sick_people = random.sample(people_indices, k=initial_seek_people)
        people_positions = [
            PeopleInitializer.__get_random_position(simulation_map)
            for _ in range(people_number)
        ]
        return [
            Person(
                person_id=person_id,
                position=position,
                sick=person_id in sick_people,
                sick_start=0 if person_id in sick_people else None
            ) for person_id, position in zip(people_indices, people_positions)
        ]


    @staticmethod
    def __get_random_position(simulation_map: Map) -> Position2D:
        x = random.randint(0, simulation_map.max_x-1)
        y = random.randint(0, simulation_map.max_y-1)
        return Position2D(x=x, y=y)
