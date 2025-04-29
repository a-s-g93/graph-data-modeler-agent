from typing import List

from ....data_dictionary.data_dictionary import TableSchema
from ...discovery.models import DiscoveryRelationship
from ..models import UpdateDataModelContext
from ..state import DataModelUpdaterSingleSourceMainState


def create_update_data_model_single_source_messages(
    state: DataModelUpdaterSingleSourceMainState,
    context: UpdateDataModelContext,
) -> list[dict]:
    """
    Create the messages for the update data model single source node.
    """

    system_message = "You are a professional graph data modeler. You are a core member of a team that will transform relational table data into a graph data model."

    user_message = """I would like you to update the following graph data model based on this provided information. Ensure that the suggested changes are implemented in the final data model.

---

**Valid Columns**
{valid_columns}

**Column Descriptions**
{column_descriptions}

**Use Cases**
{use_cases}

**Discovery Summary**
{discovery}


**Removals**
* Nodes
{nodes_to_remove}

* Relationships
{relationships_to_remove}

* Properties
{properties_to_remove}

**New Nodes**
{column_to_node_mappings}

**New Relationships**
{new_relationships}
--- 

**Rules**
{rules}


Data Model:
"""

    return [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": user_message.format(
                rules=_format_rules(context),
                valid_sources=[state["table_schema"].name],
                valid_columns=state["table_schema"].column_names,
                column_descriptions=_format_table_schema(state["table_schema"]),
                use_cases=state.get("use_cases", "No use cases provided."),
                discovery=state["discovery"].summary,
                nodes_to_remove=state["possible_updates_to_data_model"].nodes_to_remove,
                relationships_to_remove=_format_possible_relationships(state["possible_updates_to_data_model"].relationships_to_remove),
                properties_to_remove=state["possible_updates_to_data_model"].properties_to_remove,
                column_to_node_mappings=state["possible_updates_to_data_model"].column_to_node_mappings,
                new_relationships=_format_possible_relationships(state["possible_updates_to_data_model"].new_relationships),
            )
        },
    ]


def _format_table_schema(table_schema: TableSchema) -> str:
    """
    Format the table schema for the user message.
    """

    return "\n".join(
        [f"* {c}: {table_schema.get_description(c)}" for c in table_schema.column_names]
    )


def _format_rules(context: UpdateDataModelContext) -> str:
    """
    Format the rules for the user message.
    """

    rules = """
Please follow these rules strictly! Billions of dollars depend on you.

Nodes
* Each node must have a unique property
* Unique properties may be used only once per data model
* Do not group all properties into a single node
Relationships
* Relationships do NOT require uniqueness or properties
* NEVER use symmetric relationships
Properties
* A column_mapping must be an exact match to valid column
General
* Do NOT return a single-node data model"""

    if not context["allow_duplicate_column_mappings"]:
        rules += "\nAdditional Rules:"
        rules += "\n* A column may only map to a single property in the data model."

    return rules + "\n"


def _format_possible_relationships(
    possible_relationships: List[DiscoveryRelationship],
) -> str:
    """
    Format the possible relationships for the user message.
    """

    return "\n".join(
        [
            f"* (:{r['source_node_label']})-[:{r['relationship_type']}]->(:{r['target_node_label']})"
            for r in possible_relationships
        ]
    )
