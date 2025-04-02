from typing import Any, Callable, Coroutine

from instructor import AsyncInstructor

from graph_data_modeler_agent.components.discovery.models import DiscoveryResponse

from ..state import DiscoverySingleSourceMainState
from .prompts import create_generate_findings_single_source_messages


def create_generate_findings_single_source_node(
    llm_client: AsyncInstructor, model: str
) -> Callable[[DiscoverySingleSourceMainState], Coroutine[Any, Any, dict[str, Any]]]:
    """
    Create the generate findings node.
    """

    async def generate_findings_single_source(
        state: DiscoverySingleSourceMainState,
    ) -> dict[str, Any]:
        """
        Generate the findings for a single data source.
        """

        messages = create_generate_findings_single_source_messages(state)

        response = await llm_client.chat.completions.create(
            model=model, response_model=DiscoveryResponse, messages=messages
        )

        return {
            "discovery": response,
            "discovery_steps": ["generate_findings"],
        }

    return generate_findings_single_source
