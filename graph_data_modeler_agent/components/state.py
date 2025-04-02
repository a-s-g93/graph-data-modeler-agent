from operator import add
from typing import Annotated, Any, Dict, List, Optional, TypedDict

import pandas as pd

from graph_data_modeler_agent.data_model.core import DataModel


class InputState(TypedDict):
    """
    The input state of the agent.
    """

    data: List[pd.DataFrame]
    data_dictionary: Optional[Dict[str, Any]]
    use_cases: List[str]
    request: str
    steps: Annotated[List[str], add]
    next_action: str


class MainState(TypedDict):
    """
    The state of the agent.
    """

    errors: Annotated[List[str], add]
    steps: Annotated[List[str], add]
    next_action: str


class OutputState(TypedDict):
    """
    The output state of the agent.
    """

    final_model: DataModel
    sub_models: List[DataModel]
    discovery: str
    errors: Annotated[List[str], add]
    steps: Annotated[List[str], add]
