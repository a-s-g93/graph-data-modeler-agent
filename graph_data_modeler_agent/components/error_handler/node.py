from typing import Any, Callable, Coroutine

from graph_data_modeler_agent.components.state import MainState


def create_error_handler_node() -> (
    Callable[[MainState], Coroutine[Any, Any, dict[str, Any]]]
):
    """
    Create a node that handles errors.
    """

    async def error_handler_node(state: MainState) -> dict[str, Any]:
        return {"steps": ["error_handler"]}

    return error_handler_node
