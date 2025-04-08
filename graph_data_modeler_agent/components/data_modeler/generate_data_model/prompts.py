from ....data_dictionary.data_dictionary import TableSchema
from ..models import GenerateDataModelContext
from ..state import DataModelerSingleSourceMainState


def create_generate_data_model_single_source_messages(
    state: DataModelerSingleSourceMainState,
    context: GenerateDataModelContext,
) -> list[dict]:
    """
    Create the messages for the generate data model single source node.
    """

    system_message = "You are a professional graph data modeler. You are a core member of a team that will transform relational table data into a graph data model."

    user_message = """I would like you to generate a graph data model based on this provided information. Ensure that the recommended nodes are implemented in the final data model.

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

<nodes>
{nodes}
</nodes>

<possible relationships>
{possible_relationships}
</possible relationships>

<possible property keys>
{possible_property_keys}
</possible property keys>

Please return your response in json format.
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
                nodes=state["initial_nodes"],
                possible_relationships=state["discovery"].possible_relationship_types,
                possible_property_keys=state["discovery"].possible_property_keys,
                discovery=state["discovery"],
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


def _format_rules(context: GenerateDataModelContext) -> str:
    """
    Format the rules for the user message.
    """

    rules = """
Please follow these rules strictly! Billions of dollars depend on you.
Nodes
* Each node must have a unique property
* Each node must have a relationship with at least one other node
* Unique properties may NOT be shared between different nodes
* A node must only have a single ID property
Relationships
* Relationships do NOT require uniqueness or properties
* NEVER use symmetric relationships
* Do NOT create self-referential relationships
Properties
* A column_mapping must be an exact match to valid column
* A column_mapping may only be used ONCE in a data model. It may NOT be shared between nodes
General
* Do NOT return a single-node data model"""

    if not context["allow_duplicate_column_mappings"]:
        rules += "\nAdditional Rules:"
        rules += "\n* A column may only map to a single property in the data model."

    return rules + "\n"
