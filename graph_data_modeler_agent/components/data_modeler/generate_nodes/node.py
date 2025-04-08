import json
from typing import Any, Callable, Coroutine

from instructor import AsyncInstructor
from instructor.exceptions import InstructorRetryException

from graph_data_modeler_agent.data_model.core.node import Nodes

from ..models import GenerateNodesContext
from ..state import DataModelerSingleSourceInputState
from .prompts import create_generate_nodes_single_source_messages


def create_generate_nodes_single_source_node(
    llm_client: AsyncInstructor, model: str
) -> Callable[[DataModelerSingleSourceInputState], Coroutine[Any, Any, dict[str, Any]]]:
    """
    Create the generate node.
    """

    async def generate_nodes_single_source(
        state: DataModelerSingleSourceInputState,
    ) -> dict[str, Any]:
        """
        Generate the nodes for a single data source.
        """

        errors = list()

        next_data_modeler_action = "data_modeler_error_handler"

        context = GenerateNodesContext(
            table_schema=state["table_schema"],
            valid_sources=[state["table_schema"].name],
            valid_columns=state["table_schema"].column_names,
            allow_duplicate_column_mappings=True,
            enforce_uniqueness=True,
            apply_neo4j_naming_conventions=True,
        )

        messages = create_generate_nodes_single_source_messages(state, context)

        try:
            response = await llm_client.chat.completions.create(
                model=model, response_model=Nodes, messages=messages, context=context
            )

            next_data_modeler_action = "generate_data_model"

        except InstructorRetryException as e:
            errors.extend(e.messages)
            response = Nodes.model_construct(  # type: ignore
                json.loads(
                    e.last_completion.choices[-1]
                    .message.tool_calls[-1]
                    .function.arguments
                )
            )
            print("> Received Invalid Nodes")
            print(response)
            print()
        except Exception as e:
            errors.append(str(e))

        return {
            "initial_nodes": response,
            "data_modeler_steps": ["generate_nodes"],
            "errors": errors,
            "next_data_modeler_action": next_data_modeler_action,
        }

    return generate_nodes_single_source
