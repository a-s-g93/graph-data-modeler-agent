from operator import add
from typing import Annotated, Any, Dict, List, Optional, TypedDict

import pandas as pd

from graph_data_modeler_agent.components.discovery.models import DiscoveryResponse
from graph_data_modeler_agent.data_dictionary.data_dictionary import TableSchema
from graph_data_modeler_agent.data_model.core import DataModel


class MultiSourceInputState(TypedDict):
    """
    The input state of the multi source agent.
    """

    data: List[pd.DataFrame]
    data_dictionary: Optional[Dict[str, Any]]
    use_cases: List[str]
    additional_context: str
    steps: Annotated[List[Any], add]
    next_action: str


class MultiSourceMainState(TypedDict):
    """
    The state of the multi source agent.
    """

    errors: Annotated[List[str], add]
    steps: Annotated[List[Any], add]
    next_action: str


class MultiSourceOutputState(TypedDict):
    """
    The output state of the multi source agent.
    """

    final_model: DataModel
    sub_models: List[DataModel]
    discovery: List[DiscoveryResponse]
    errors: Annotated[List[str], add]
    steps: Annotated[List[Any], add]


class SingleSourceInputState(TypedDict):
    """
    The input state of the single source agent.
    """

    data: Optional[pd.DataFrame]
    table_schema: Dict[str, Any]
    use_cases: List[str]
    additional_context: str


class SingleSourceMainState(TypedDict):
    """
    The state of the single source agent.
    """

    data_model: DataModel
    discovery: DiscoveryResponse
    table_schema: TableSchema
    use_cases: List[str]
    additional_context: str
    errors: Annotated[List[str], add]
    steps: Annotated[List[Any], add]


class SingleSourceOutputState(TypedDict):
    """
    The output state of the single source agent.
    """

    data_model: DataModel
    discovery: DiscoveryResponse
    table_schema: TableSchema
    use_cases: List[str]
    additional_context: str
    errors: Annotated[List[str], add]
    steps: Annotated[List[Any], add]
