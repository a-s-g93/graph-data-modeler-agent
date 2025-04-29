from operator import add
from typing import Annotated, List, TypedDict

from pydantic import Field

from ...data_dictionary.data_dictionary import TableSchema
from ...data_model.core.data_model import DataModel
from .brainstorm_updates.models import DataModelUpdaterBrainstormResponse
from ..discovery.models import DiscoveryResponse

class DataModelUpdaterSingleSourceInputState(TypedDict):
    """
    The input state of the data model updater component.
    """

    data_model: DataModel = Field(
        ..., description="The generated data model."
    )
    table_schema: TableSchema = Field(
        ..., description="The table schema of the data to be added to the data model."
    )
    use_cases: List[str] = Field(
        ..., description="The use cases the graph data model should address."
    )
    discovery: DiscoveryResponse = Field(
        ..., description="The discovery of the data."
    )
    additional_context: str = Field(..., description="Additional context.")
    data_model_updater_steps: Annotated[List[str], add] = Field(
        ..., description="The data model updater steps."
    )


class DataModelUpdaterSingleSourceMainState(TypedDict):
    """
    The main state of the data model updater component.
    """

    data_model: DataModel
    errors: List[str]
    possible_updates_to_data_model: DataModelUpdaterBrainstormResponse
    table_schema: TableSchema
    use_cases: List[str]
    discovery: DiscoveryResponse
    additional_context: str
    data_model_updater_steps: Annotated[List[str], add]
    next_data_model_updater_action: str


class DataModelUpdaterSingleSourceOutputState(TypedDict):
    """
    The output state of the data model updater component.
    """

    data_model: DataModel
    possible_updates_to_data_model: DataModelUpdaterBrainstormResponse
    table_schema: TableSchema
    use_cases: List[str]
    discovery: DiscoveryResponse
    additional_context: str
    data_model_updater_steps: Annotated[List[str], add]
