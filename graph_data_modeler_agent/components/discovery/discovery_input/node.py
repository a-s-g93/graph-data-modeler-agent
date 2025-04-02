from typing import Any, Callable, Coroutine

from ..state import DiscoverySingleSourceInputState


def create_discovery_input_node() -> (
    Callable[[DiscoverySingleSourceInputState], Coroutine[Any, Any, dict[str, Any]]]
):
    """
    Create the discovery input node.
    """

    async def discovery_input(state: DiscoverySingleSourceInputState) -> dict[str, Any]:
        """
        Assess the input provided to the discovery agent. If no data is provided, then skip the Pandas stats generation step.
        """

        steps = ["discovery_input"]

        if state.get("data") is None:
            return {
                "next_discovery_action": "generate_findings",
                "discovery_steps": steps,
            }

        return {"next_discovery_action": "generate_stats", "discovery_steps": steps}

    return discovery_input
