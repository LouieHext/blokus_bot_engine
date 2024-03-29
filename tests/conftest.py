"""
Date    :   2024/01/29
Author  :   Louie Hext
License :   (C)Copyright 2024, A-Space
"""
import json
import os

# Python Imports
from pathlib import Path

import pytest

# External Imports
from data_structures.graph import Graph

# Internal Imports


"""
This is a configuration file for pytest containing customizations and fixtures.
"""

DATA_DIRECTORY = Path(os.environ["TEST_DATA_DIRECTORY_LIVINGROOM_FURNISHER"])


@pytest.fixture(params=DATA_DIRECTORY.glob("floorplan_graph*.json"))
def graph(request) -> Graph:
    """graph loaded directly from a json file.

    Returns:
        Graph:graph loaded from a json file
    """
    print(request)
    with open(request.param, "r") as f:
        data = json.load(f)
    return Graph.from_json(data)
