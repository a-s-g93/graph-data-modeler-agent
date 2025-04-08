from typing import List

from ....data_dictionary.data_dictionary import TableSchema
from ...discovery.models import ColumnToNodeMapping
from ..models import GenerateNodesContext
from ..state import DataModelerSingleSourceInputState


def create_generate_nodes_single_source_messages(
    state: DataModelerSingleSourceInputState,
    context: GenerateNodesContext,
) -> list[dict]:
    """
    Create the messages for the generate nodes single source node.
    """

    system_message = "You are a professional graph data modeler. You are a core member of a team that will transform relational table data into a graph data model."

    user_message = """I would like you to generate a list of nodes for a graph data model based on this provided information. We will add relationships in the next step.

---

Each column may be used ONCE in the data model.
**Column Descriptions**
{column_descriptions}

**Use Cases**
{use_cases}

**Discovery Summary**
{discovery}

**Possible Node Labels**
{possible_nodes}

**Column to Node Mappings**
{column_to_node_mappings}

--- 

**CRITICAL RULES (do not break these):**
{rules}

**Output Format**
{output_format}

Nodes:
"""

    return [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": user_message.format(
                rules=_format_rules(context),
                valid_sources=context["valid_sources"],
                valid_columns=context["valid_columns"],
                column_descriptions=_format_table_schema(state["table_schema"]),
                discovery=state["discovery"].summary,
                column_to_node_mappings=_format_column_to_node_mappings(
                    state["discovery"].column_to_node_mappings
                ),
                possible_nodes=state["discovery"].possible_node_labels,
                possible_property_keys=state["discovery"].possible_property_keys,
                use_cases=state.get("use_cases", "No use cases provided."),
                output_format=get_output_format(),
            ),
        },
    ]


def _format_table_schema(table_schema: TableSchema) -> str:
    """
    Format the table schema for the user message.
    """

    return "\n".join(
        [f"* {c}: {table_schema.get_description(c)}" for c in table_schema.column_names]
    )


def _format_rules(context: GenerateNodesContext) -> str:
    """
    Format the rules for the user message.
    """

    rules = """Please follow these rules strictly! Billions of dollars depend on you.
* Each node must have a property marked as `"is_key": true`.
* Key properties must **never** be shared between nodes.
* All nodes should have **at least one property**, and no node should contain all properties.
* Use the `column_to_node_mappings` to determine which columns to use for each node.

    """

    if not context["allow_duplicate_column_mappings"]:
        rules += "\n* A column name may only be used as a `Property`.`column_mapping` value once."
        rules += "\n* Each `column_mapping` value (e.g., 'id', 'title', etc.) **MUST be used only once** in the entire model."
        rules += "\n* Nodes **may NOT share column mappings** — each property must map to a **unique source column**."

    return rules


def _format_column_to_node_mappings(
    column_to_node_mappings: List[ColumnToNodeMapping],
) -> str:
    """
    Format the column to node mappings for the user message.
    """
    res = "  column_name: node_label\n"
    return res + "\n".join(
        [f"* {m['column_name']}: {m['node_label']}" for m in column_to_node_mappings]
    )


def get_output_format() -> str:
    return """Property Format:
{
    "name": <`Property` name>,
    "type": <Python type>,
    "column_mapping": <source column that maps to `Property`>,
    "alias": <a foreign key column from another source file that maps to `Property`>,
    "is_key": <`Property` is a unique identifier>,
}

Node Format:
{
    "label": <node label>,
    "properties": <list of Property>,
    "source_name": <source file name>
}"""
