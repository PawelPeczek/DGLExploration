from typing import List, Dict, Any

from src.utils.fs_utils import dump_json_to_file
from src.virus_simulation.primitives import SimulationState, Person, Meeting
import src.virus_simulation.config as simulation_config


def convert_simulation_state_to_json(simulation_state: SimulationState,
                                     target_path: str
                                     ) -> None:
    vertices = prepare_vertices(simulated_people=simulation_state.people)
    edges = prepare_edges(simulated_meetings=simulation_state.meetings)
    converted_graph = {
        simulation_config.GRAPH_VERTICES_KEY: vertices,
        simulation_config.GRAPH_EDGES_KEY: edges
    }
    dump_json_to_file(
        target_path=target_path,
        content=converted_graph
    )


def prepare_vertices(simulated_people: List[Person]) -> List[Dict[str, Any]]:
    return [
        {
            simulation_config.PERSON_ID_KEY: person.person_id,
            simulation_config.SICKNESS_STATUS_KEY: person.sick
        } for person in simulated_people
    ]


def prepare_edges(simulated_meetings: List[Meeting]) -> List[Dict[str, Any]]:
    return [
        {
            simulation_config.MEETING_PAIR_KEY: meeting.get_pair_ids(),
            simulation_config.MEETING_DURATION_KEY: meeting.duration,
            simulation_config.MEETING_TIME_STAMP_KEY: meeting.time_stamp
        } for meeting in simulated_meetings
    ]
