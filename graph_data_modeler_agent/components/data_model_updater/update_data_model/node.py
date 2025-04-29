import json
from typing import Any, Callable, Coroutine

from instructor import AsyncInstructor
from instructor.exceptions import InstructorRetryException

from graph_data_modeler_agent.data_model.core.data_model import DataModel

from ..models import UpdateDataModelContext
from ..state import DataModelUpdaterSingleSourceMainState
from .prompts import create_update_data_model_single_source_messages


def create_update_data_model_single_source_node(
    llm_client: AsyncInstructor, model: str
) -> Callable[[DataModelUpdaterSingleSourceMainState], Coroutine[Any, Any, dict[str, Any]]]:
    """
    Create the update data model node.
    """

    async def update_data_model_single_source(
        state: DataModelUpdaterSingleSourceMainState,
    ) -> dict[str, Any]:
        """
        Update the data model for a single data source.
        """

        errors = list()

        next_data_modeler_action = "data_modeler_error_handler"

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
            valid_sources=[state["table_schema"].name],
        )

        messages = create_update_data_model_single_source_messages(state, context)
        response = None

        try:
            response = await llm_client.chat.completions.create(
                model=model,
                response_model=DataModel,
                messages=messages,
                context=context,
            )

            next_data_modeler_action = "__end__"

        # if the generation fails, we want to return the original data model
        except InstructorRetryException as e:
            errors.extend(e.messages)
            response = state["data_model"]

        except Exception as e:
            errors.append(str(e))
            response = state["data_model"]
            
        return {
            "data_model": response,
            "data_model_updater_steps": ["update_data_model"],
            "errors": errors,
            "next_data_model_updater_action": next_data_modeler_action,
        }

    return update_data_model_single_source
