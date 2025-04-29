from typing import Dict, List, TypedDict

from ...data_dictionary.table_schema import TableSchema


class GenerateNodesContext(TypedDict):
    """
    Context for `Nodes` validation.

    Attributes
    ----------
    table_schema : TableSchema
        The table schema containing columns and descriptions.
    valid_sources : List[str]
        The valid sources allowed.
    valid_columns : List[str]
        The valid columns allowed per file.
    enforce_uniqueness : bool
        Whether to enforce Node uniqueness
    apply_neo4j_naming_conventions : bool
        Whether to apply Neo4j naming conventions
    allow_duplicate_column_mappings : bool
        Whether to allow a column to be mapped to many Properties
    """

    table_schema: TableSchema
    valid_sources: List[str]
    valid_columns: List[str]
    enforce_uniqueness: bool
    apply_neo4j_naming_conventions: bool
    allow_duplicate_column_mappings: bool


class GenerateDataModelContext(GenerateNodesContext):
    """
    Context for `DataModel` validation.

    Attributes
    ----------
    table_schema : TableSchema
        The table schema containing columns and descriptions.
    valid_sources : List[str]
        The valid sources allowed.
    valid_columns : List[str]
        The valid columns allowed per file.
    enforce_uniqueness : bool
        Whether to enforce Node uniqueness
    apply_neo4j_naming_conventions : bool
        Whether to apply Neo4j naming conventions
    allow_duplicate_column_mappings : bool
        Whether to allow a column to be mapped to many Properties
    allow_parallel_relationships : bool
        Whether to allow parallel relationships (same and opposite direction)
    allow_relationships_between_same_node_label : bool
        Whether to allow relationships between the same node label. For example (:Person)-[:KNOWS]->(:Person)
    """

    allow_parallel_relationships: bool
    allow_relationships_between_same_node_label: bool
