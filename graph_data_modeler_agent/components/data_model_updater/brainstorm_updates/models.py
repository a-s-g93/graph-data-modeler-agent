from typing_extensions import List, TypedDict

from pydantic import BaseModel, Field, field_validator

from ....components.discovery.models import DiscoveryRelationship, ColumnToNodeMapping


class UpdaterProperty(TypedDict):
    """
    A property to be added to a node.
    """

    label_or_type: str = Field(
        ..., description="The node label or relationship type containing the property."
    )
    property_name: str = Field(..., description="The name of the property in Neo4j.")
    reason: str = Field(..., description="An explanation for this suggestion.")


class UpdaterNode(TypedDict):
    """
    A node to be added to the data model.
    """

    label: str = Field(..., description="The label of the node.")
    reason: str = Field(..., description="An explanation for this suggestion.")


class UpdaterRelationship(DiscoveryRelationship):
    """
    A relationship to be added to the data model.
    """

    reason: str = Field(..., description="An explanation for this suggestion.")


class DataModelUpdaterBrainstormResponse(BaseModel):
    """
    Response from `DataModelUpdater`.
    """

    nodes_to_remove: List[UpdaterNode] = Field(
        default=list(), description="The nodes to remove from the data model, if any."
    )

    relationships_to_remove: List[UpdaterRelationship] = Field(
        default=list(), description="The relationships to remove from the data model, if any."
    )

    properties_to_remove: List[UpdaterProperty] = Field(
        default=list(), description="The properties to remove from the data model, if any."
    )

    column_to_node_mappings: List[ColumnToNodeMapping] = Field(
        ...,    
        description="A mapping of column names to node labels. This is used to ensure that each column is only used once in the graph data model.",
    )

    new_relationships: List[DiscoveryRelationship] = Field(
        default=list(), description="The new relationships to add to the data model, if any."
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
