import logging
import os

RESOURCES_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "resources")
)
VIRUS_SIMULATION_OUTPUT_PATH = os.path.join(
    RESOURCES_PATH, "virus_simulation_output"
)
LOGGING_LEVEL = logging.INFO
