from operator import add
from typing import Annotated, List, TypedDict

from ...data_dictionary.data_dictionary import TableSchema
from ...data_model.core.data_model import DataModel
from ...data_model.core.node import Nodes
from ..discovery.models import DiscoveryResponse


class DataModelerSingleSourceInputState(TypedDict):
    """
    The input state of the data modeler component.
    """

    discovery: DiscoveryResponse
    table_schema: TableSchema
    use_cases: List[str]
    additional_context: str
    data_modeler_steps: Annotated[List[str], add]


class DataModelerSingleSourceMainState(TypedDict):
    """
    The main state of the data modeler component.
    """

    initial_nodes: Nodes
    data_model: DataModel
    errors: List[str]
    discovery: DiscoveryResponse
    table_schema: TableSchema
    use_cases: List[str]
    additional_context: str
    data_modeler_steps: Annotated[List[str], add]
    next_data_modeler_action: str


class DataModelerSingleSourceOutputState(TypedDict):
    """
    The output state of the data modeler component.
    """

    initial_nodes: Nodes
    data_model: DataModel
    errors: List[str]
    discovery: DiscoveryResponse
    table_schema: TableSchema
    use_cases: List[str]
    additional_context: str
    data_modeler_steps: Annotated[List[str], add]
