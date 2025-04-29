from ....data_dictionary.data_dictionary import TableSchema
from ..models import UpdateDataModelContext
from ..state import DataModelUpdaterSingleSourceMainState
from ...data_modeler.generate_data_model.prompts import _format_rules

def create_brainstorm_updates_to_data_model_messages(
    state: DataModelUpdaterSingleSourceMainState,
    context: UpdateDataModelContext,
) -> list[dict]:
    """
    Create the messages for the brainstorm updates to the data model node.
    """

    system_message = "You are a professional graph data modeler. You are a core member of a team that will transform relational table data into a graph data model."

    user_message = """I would like you to brainstorm updates to a graph data model based on this provided information. 
This suggestions should satisfy the use cases and rules provided. 
Only information from the provided columns may be used to update the data model.

---

**Valid Columns**
{valid_columns}

**Column Descriptions**
{column_descriptions}

**Data Model**
{data_model}

--- 

Focus on the following use cases!
**Use Cases**
{use_cases}

**Rules**
{rules}


What nodes or relationships should be added?
What nodes or relationships should be removed?
How can the this model be improved?
Suggested Updates:
"""

    return [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": user_message.format(
                rules=_format_rules(context),
                valid_columns=state["table_schema"].column_names,
                column_descriptions=_format_table_schema(state["table_schema"]),
                use_cases=state.get("use_cases", "No use cases provided."),
                data_model=state["data_model"].get_schema(),
               
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


# def _format_rules(context: UpdateDataModelContext) -> str:
#     """
#     Format the rules for the user message.
#     """

#     rules = """
# Please follow these rules strictly! Billions of dollars depend on you.

# ** Do not modify the provided nodes. **

# Nodes
# * Each node must have a unique property
# * Unique properties may be used only once per data model
# * Do not group all properties into a single node
# Relationships
# * Relationships do NOT require uniqueness or properties
# * NEVER use symmetric relationships
# Properties
# * A column_mapping must be an exact match to valid column
# General
# * Do NOT return a single-node data model"""

#     if not context["allow_duplicate_column_mappings"]:
#         rules += "\nAdditional Rules:"
#         rules += "\n* A column may only map to a single property in the data model."

#     return rules + "\n"
