from typing import Any, Callable, Coroutine

from ..state import DataModelerSingleSourceMainState


def create_data_modeler_error_handler_node() -> (
    Callable[[DataModelerSingleSourceMainState], Coroutine[Any, Any, dict[str, Any]]]
):
    """
    Create the data modeler error handler node.
    """

    def data_modeler_error_handler(
        state: DataModelerSingleSourceMainState,
    ) -> dict[str, Any]:
        """
        Handle the data modeler errors.
        """

        # Do Something

        return {
            "data_modeler_steps": ["data_modeler_error_handler"],
            "next_data_modeler_action": "__end__",
        }

    return data_modeler_error_handler
