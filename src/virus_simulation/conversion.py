from typing import List, Dict, Any

from src.utils.fs_utils import dump_json_to_file
from src.virus_simulation.primitives import SimulationState, Person, Contact, \
    Position2D, CompactPosition2D
import src.virus_simulation.config as simulation_config


def convert_simulation_state_to_json(simulation_state: SimulationState,
                                     target_path: str
                                     ) -> None:
    map_dimensions = simulation_state.map.max_x, simulation_state.map.max_y
    vertices = prepare_vertices(simulated_people=simulation_state.people)
    edges = prepare_edges(simulated_meetings=simulation_state.meetings)
    people_traces = prepare_people_traces(
        people_traces=simulation_state.people_traces
    )
    converted_graph = {
        simulation_config.MAP_DIMENSIONS_KEY: map_dimensions,
        simulation_config.GRAPH_VERTICES_KEY: vertices,
        simulation_config.GRAPH_EDGES_KEY: edges,
        simulation_config.PEOPLE_TRACES_KEY: people_traces
    }
    dump_json_to_file(
        target_path=target_path,
        content=converted_graph
    )


def prepare_vertices(simulated_people: List[Person]) -> List[Dict[str, Any]]:
    return [
        {
            simulation_config.PERSON_ID_KEY: person.person_id,
            simulation_config.SICKNESS_STATUS_KEY: person.sick,
            simulation_config.SICKNESS_START_KEY: person.sick_start
        } for person in simulated_people
    ]


def prepare_edges(simulated_meetings: List[Contact]) -> List[Dict[str, Any]]:
    return [
        {
            simulation_config.CONTACT_PAIR_KEY: meeting.get_pair_ids(),
            simulation_config.CONTACT_DURATION_KEY: meeting.intensity,
            simulation_config.CONTACT_TIME_STAMP_KEY: meeting.time_stamp
        } for meeting in simulated_meetings
    ]


def prepare_people_traces(people_traces: Dict[Person, List[Position2D]]
                          ) -> Dict[int, List[CompactPosition2D]]:
    return {
        person.person_id: [position.tu_tuple() for position in person_trace]
        for person, person_trace in people_traces.items()
    }
