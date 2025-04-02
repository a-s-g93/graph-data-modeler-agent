from typing import List, TypedDict

import pandas as pd
from pydantic import BaseModel, Field


class DiscoveryResponse(BaseModel):
    """
    The response from the discovery agent. This response will inform the graph data modeling process.
    """

    summary: str = Field(
        ...,
        description="A summary of the data that will intellectually inform the graph data modeling process.",
    )
    possible_node_labels: List[str] = Field(
        ..., description="The possible node labels identified in the data."
    )
    possible_relationship_types: List[str] = Field(
        ..., description="The possible relationship types identified in the data."
    )
    possible_property_keys: List[str] = Field(
        ...,
        description="The possible property keys identified in the data. These may be used to identify unique nodes in the graph.",
    )


class PandasStatsResponse(TypedDict):
    """
    The response from the pandas stats process.
    """

    general_description: str
    categorical_description: pd.DataFrame
    numerical_description: pd.DataFrame
