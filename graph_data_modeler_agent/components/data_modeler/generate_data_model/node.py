from typing import Any, Callable, Coroutine

from instructor import AsyncInstructor
from instructor.exceptions import InstructorRetryException

from graph_data_modeler_agent.data_model.core.data_model import DataModel

from ..models import GenerateDataModelContext
from ..state import DataModelerSingleSourceMainState
from .prompts import create_generate_data_model_single_source_messages


def create_generate_data_model_single_source_node(
    llm_client: AsyncInstructor, model: str
) -> Callable[[DataModelerSingleSourceMainState], Coroutine[Any, Any, dict[str, Any]]]:
    """
    Create the generate data model node.
    """

    async def generate_data_model_single_source(
        state: DataModelerSingleSourceMainState,
    ) -> dict[str, Any]:
        """
        Generate the data model for a single data source.
        """

        errors = list()

        next_data_modeler_action = "data_modeler_error_handler"

        context = GenerateDataModelContext(
            table_schema=state["table_schema"],
            valid_columns=state["table_schema"].column_names,
            allow_duplicate_column_mappings=True,
            enforce_uniqueness=True,
            apply_neo4j_naming_conventions=True,
            allow_parallel_relationships=False,
        )

        messages = create_generate_data_model_single_source_messages(state, context)

        try:
            response = await llm_client.chat.completions.create(
                model=model,
                response_model=DataModel,
                messages=messages,
                context=context,
            )

            next_data_modeler_action = "__end__"

        except InstructorRetryException as e:
            errors.extend(e.messages)

        except Exception as e:
            errors.append(str(e))

        return {
            "data_model": response,
            "data_modeler_steps": ["generate_data_model"],
            "errors": errors,
            "next_data_modeler_action": next_data_modeler_action,
        }

    return generate_data_model_single_source
