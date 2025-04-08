import pandas as pd
from pydantic import BaseModel, Field, field_validator
from typing_extensions import List, TypedDict


class ColumnToNodeMapping(TypedDict):
    """
    A mapping of column names to node labels. This is used to ensure that each column is only used once in the graph data model.
    """

    column_name: str
    node_label: str


class DiscoveryResponse(BaseModel):
    """
    The response from the discovery agent. This response will inform the graph data modeling process.
    """

    summary: str = Field(
        ...,
        description="""A summary of the data that will intellectually inform the graph data modeling process. 
This should contain reasoning behind why node labels and relationship types were chosen as well as why the property keys are significant. 
Why is this information important to include in the graph data model?""",
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
    column_to_node_mappings: List[ColumnToNodeMapping] = Field(
        ...,
        description="A mapping of column names to node labels. This is used to ensure that each column is only used once in the graph data model.",
    )

    @field_validator("column_to_node_mappings")
    def validate_column_to_node_mappings(
        cls, v: List[ColumnToNodeMapping]
    ) -> List[ColumnToNodeMapping]:
        """
        Validate the column to node mappings.
        """

        counts = {m["column_name"]: 0 for m in v}
        for m in v:
            counts[m["column_name"]] += 1
        errors = list()
        for column_name, count in counts.items():
            if count > 1:
                errors.append(column_name)
        if len(errors) > 0:
            raise ValueError(f"Columns {errors} are mapped to multiple node labels.")
        return v


class PandasStatsResponse(TypedDict):
    """
    The response from the pandas stats process.
    """

    general_description: str
    categorical_description: pd.DataFrame
    numerical_description: pd.DataFrame
