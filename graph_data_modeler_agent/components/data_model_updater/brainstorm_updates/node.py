from typing import Any, Callable, Coroutine

from instructor import AsyncInstructor

from ..state import DataModelUpdaterSingleSourceMainState
from .models import DataModelUpdaterBrainstormResponse
from .prompts import create_brainstorm_updates_to_data_model_messages
from ..models import UpdateDataModelContext

def create_brainstorm_updates_single_source_node(
    llm_client: AsyncInstructor, model: str, max_retries: int = 3
) -> Callable[[DataModelUpdaterSingleSourceMainState], Coroutine[Any, Any, dict[str, Any]]]:
    """
    Create the brainstorm updates to the data model node.
    """

    async def brainstorm_updates_to_data_model(
        state: DataModelUpdaterSingleSourceMainState,
    ) -> dict[str, Any]:
        """
        Brainstorm updates to the data model.
        """

        context = UpdateDataModelContext(
            table_schema=state["table_schema"],
            valid_columns=state["table_schema"].column_names,
            allow_duplicate_column_mappings=False,
            table_column_listings={
                state["table_schema"].name: state["table_schema"].column_names
            },
            enforce_uniqueness=True,
            apply_neo4j_naming_conventions=True,
            allow_parallel_relationships=False,
            allow_relationships_between_same_node_label=True,
        )
        messages = create_brainstorm_updates_to_data_model_messages(state, context)

        response = await llm_client.chat.completions.create(
            model=model,
            response_model=DataModelUpdaterBrainstormResponse,
            messages=messages,
            max_retries=max_retries,
        )

        return {
            "possible_updates_to_data_model": response,
            "data_model_updater_steps": ["brainstorm_updates"],
        }

    return brainstorm_updates_to_data_model
