from typing import Any, Callable, Coroutine

from graph_data_modeler_agent.components.state import InputState
from graph_data_modeler_agent.data_dictionary.data_dictionary import DataDictionary


def create_input_validator_node() -> (
    Callable[[InputState], Coroutine[Any, Any, dict[str, Any]]]
):
    """
    Create a node that validates the input state.
    """

    async def input_validator(state: InputState) -> dict[str, Any]:
        try:
            data_dictionary = DataDictionary.model_validate(state["data_dictionary"])
            return {
                "data_dictionary": data_dictionary,
                "next_action": "discovery",
                "steps": ["input_validator"],
            }
        except Exception as e:
            error = f"Invalid data dictionary: {e}"
            return {
                "error": error,
                "next_action": "error_handler",
                "steps": ["input_validator"],
            }

    return input_validator
