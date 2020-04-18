from __future__ import annotations

from copy import deepcopy
from typing import Dict, Any, Tuple, List

import numpy as np

from src.utils.fs_utils import parse_json
import src.virus_simulation.config as simulation_config
from src.utils.iterables import unzip_list
from src.virus_simulation.errors import SnapshotParsingError
from src.virus_simulation.primitives import CompactPosition2D


class Snapshot:

    __REQUIRED_KEYS = [
        simulation_config.MAP_DIMENSIONS_KEY,
        simulation_config.PEOPLE_TRACES_KEY,
        simulation_config.GRAPH_EDGES_KEY,
        simulation_config.GRAPH_VERTICES_KEY
    ]

    @classmethod
    def initialize(cls, snapshot_path: str) -> Snapshot:
        snapshot_json = parse_json(json_path=snapshot_path)
        cls.__check_snapshot_consistency(snapshot_json=snapshot_json)
        return cls(snapshot_json=snapshot_json)

    @classmethod
    def __check_snapshot_consistency(cls, snapshot_json: Dict[str, Any]) -> None:
        if any(k not in snapshot_json for k in Snapshot.__REQUIRED_KEYS):
            raise SnapshotParsingError(
                f"One of required keys ({Snapshot.__REQUIRED_KEYS}) missing."
            )

    def __init__(self, snapshot_json: Dict[str, Any]):
        self.__snapshot_json = snapshot_json

    @property
    def traces(self) -> Dict[int, Tuple[np.ndarray, np.ndarray]]:
        return {
            int(person_id): self.__prepare_trace_arrays(person_trace=person_trace)
            for person_id, person_trace in
            self.__snapshot_json.get(simulation_config.PEOPLE_TRACES_KEY, {}).items()
        }

    @property
    def people(self) -> List[dict]:
        return deepcopy(
            self.__snapshot_json.get(simulation_config.GRAPH_VERTICES_KEY, [])
        )

    @property
    def contacts(self) -> List[dict]:
        return deepcopy(
            self.__snapshot_json.get(simulation_config.GRAPH_EDGES_KEY, [])
        )

    def __prepare_trace_arrays(self,
                               person_trace: List[CompactPosition2D]
                               ) -> Tuple[np.ndarray, np.ndarray]:
        x_coords, y_coords = unzip_list(to_unzip=person_trace)
        return np.array(x_coords, dtype=np.uint16), np.array(y_coords, dtype=np.uint16)
