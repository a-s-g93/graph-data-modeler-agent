from operator import add
from typing import Annotated, List, Optional, TypedDict

import pandas as pd

from ...data_dictionary.data_dictionary import TableSchema
from .models import DiscoveryResponse, PandasStatsResponse


class DiscoverySingleSourceInputState(TypedDict):
    """
    The input state of the discovery agent. The discovery agent handles a single DataFrame at a time.
    """

    data: Optional[pd.DataFrame]
    table_schema: TableSchema
    use_cases: List[str]
    additional_context: str
    discovery_steps: Annotated[List[str], add]
    next_discovery_action: str


class DiscoverySingleSourceMainState(TypedDict):
    """
    The main state of the discovery agent.
    """

    data: Optional[pd.DataFrame]
    table_schema: TableSchema
    use_cases: List[str]
    additional_context: str
    stats: Optional[PandasStatsResponse]
    discovery: DiscoveryResponse
    errors: Annotated[List[str], add]
    discovery_steps: Annotated[List[str], add]
    next_discovery_action: str


class DiscoverySingleSourceOutputState(TypedDict):
    """
    The output state of the discovery component.
    """

    discovery: DiscoveryResponse
    table_schema: TableSchema
    use_cases: List[str]
    additional_context: str
    discovery_steps: Annotated[List[str], add]
