import argparse
import os
from typing import Set

from tqdm import tqdm
import logging

from src.virus_simulation.conversion import convert_simulation_state_to_json
from src.virus_simulation.engine import SimulationEngine
import src.config as global_config


logging.getLogger().setLevel(global_config.LOGGING_LEVEL)


def execute_simulation(simulation_engine: SimulationEngine,
                       simulation_name: str,
                       steps: int,
                       snapshot_steps: Set[int]) -> None:
    for step in tqdm(range(steps)):
        simulation_engine.take_simulation_step()
        if step in snapshot_steps:
            _persist_simulation_state(
                simulation_engine=simulation_engine,
                simulation_name=simulation_name,
                step=step
            )
    _persist_simulation_state(
        simulation_engine=simulation_engine,
        simulation_name=simulation_name,
        step=steps-1
    )


def _persist_simulation_state(simulation_engine: SimulationEngine,
                              simulation_name: str,
                              step: int
                              ) -> None:
    simulation_state = simulation_engine.get_simulation_state()
    target_path = os.path.join(
        global_config.VIRUS_SIMULATION_OUTPUT_PATH,
        f"{simulation_name}_snapshot_{step}.json"
    )
    logging.info(f"[Step #{step}]Persisting snapshot under {target_path}")
    convert_simulation_state_to_json(
        simulation_state=simulation_state,
        target_path=target_path
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        "Graph data generator from simple simulation of virus expansion"
    )
    parser.add_argument(
        "--map_size",
        help="Size of map to place people.",
        type=int,
        required=True
    )
    parser.add_argument(
        "--people_number",
        help="Number of people to place on map.",
        type=int,
        required=True
    )
    parser.add_argument(
        "--simulation_name",
        help="Distinguishable name of simulation.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--steps",
        help="Number of steps to carry on the simulation.",
        type=int,
        default=100
    )
    parser.add_argument(
        "--snapshot_steps",
        help="Intermediate steps to take snapshots of simulation state.",
        type=int,
        nargs="*",
        default=[]
    )
    parser.add_argument(
        "--transmission_probability",
        help="Probability of virus transmission.",
        type=float,
        default=0.5
    )
    parser.add_argument(
        "--initial_seek_people",
        help="Number of people sick at zero-day.",
        type=int,
        default=1
    )

    args = parser.parse_args()

    simulation_engine = SimulationEngine.initialize(
        map_size=args.map_size,
        people_number=args.people_number,
        initial_seek_people=args.initial_seek_people,
        transmission_probability=args.transmission_probability
    )
    execute_simulation(
        simulation_engine=simulation_engine,
        simulation_name=args.simulation_name,
        steps=args.steps,
        snapshot_steps=set(args.snapshot_steps)
    )
