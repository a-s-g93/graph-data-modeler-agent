from ....data_dictionary.data_dictionary import TableSchema
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


<rules>
{rules}
</rules>

<valid columns>
{valid_columns}
</valid columns>

<column descriptions>
{column_descriptions}
</column descriptions>

<use cases>
{use_cases}
</use cases>

<discovery>
{discovery}
</discovery>

<possible nodes>
{possible_nodes}
</possible nodes>

<possible property keys>
{possible_property_keys}
</possible property keys>

Please return your response in json format.
<format>
{output_format}
</format>


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
                discovery=state["discovery"],
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
* Each node must have a unique property
* Unique properties may NOT be duplicated
"""

    if not context["allow_duplicate_column_mappings"]:
        rules += "\n* A column may only be used once in the nodes list."
        rules += "\n* Do not duplicate column mappings."

    return rules


def get_output_format() -> str:
    return """Property Format:
{
    "name": <`Property` name>,
    "type": <Python type>,
    "column_mapping": <csv column that maps to `Property`>,
    "alias": <a second column that maps to `Property`. identifies relationship between two nodes of the same label or a relationship that spans across different files>,
    "is_unique": <`Property` is a unique identifier>,
    "part_of_key": <`Property` that with at least 1 other `Property`, makes a unique combination>
}

Node Format:
{
    "label": <node label>,
    "properties": <list of Property>,
    "source_name": <source file name>
}"""
