from ....data_dictionary.data_dictionary import TableSchema
from ..state import DiscoverySingleSourceMainState


def create_generate_findings_single_source_messages(
    state: DiscoverySingleSourceMainState,
) -> list[dict]:
    """
    Create the messages for the generate findings single source node.
    """

    system_message = "You are a professional graph data analyst. You are a core member of a team that will transform relational table data into a graph data model."

    user_message = """
Please perform an anlysis of the following data table information. 
Create a summary of the data that will intellectually inform the graph data modeling process.
Identify possible node labels, relationship types, and key properties that will be used in the graph data model.

<table_summary>
{table_summary}
</table_summary>

<use_cases>
{use_cases}
</use_cases>

<table_stats>
{table_stats}
</table_stats>

<column_descriptions>
{column_descriptions}
</column_descriptions>

Please return your response in json format.
"""

    return [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": user_message.format(
                table_summary=state.get(
                    "data_description", "No data description provided."
                ),
                use_cases=state.get("use_cases", "No use cases provided."),
                table_stats=state.get("table_stats", "No stats provided."),
                column_descriptions=_format_table_schema(state["table_schema"]),
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
