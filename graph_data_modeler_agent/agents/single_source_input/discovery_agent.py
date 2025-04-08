from typing import Literal

from instructor import AsyncInstructor
from langgraph.constants import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph

from ...components.discovery import (
    create_discovery_input_node,
    create_generate_findings_single_source_node,
    create_generate_stats_single_source_node,
)
from ...components.discovery.state import (
    DiscoverySingleSourceInputState,
    DiscoverySingleSourceMainState,
    DiscoverySingleSourceOutputState,
)


def create_discovery_agent(
    llm_client: AsyncInstructor, model: str
) -> CompiledStateGraph:
    """
    Create a discovery agent that will generate a graph data model from a single source.
    """

    graph = StateGraph(
        input=DiscoverySingleSourceInputState,
        state_schema=DiscoverySingleSourceMainState,
        output=DiscoverySingleSourceOutputState,
    )

    generate_stats = create_generate_stats_single_source_node()
    generate_findings = create_generate_findings_single_source_node(
        llm_client=llm_client, model=model
    )
    discovery_input = create_discovery_input_node()

    graph.add_node("discovery_input", discovery_input)
    graph.add_node("generate_stats", generate_stats)
    graph.add_node("generate_findings", generate_findings)

    graph.add_edge(START, "discovery_input")
    graph.add_conditional_edges(
        "discovery_input",
        discovery_router,
        {"generate_stats": "generate_stats", "generate_findings": "generate_findings"},
    )
    graph.add_edge("generate_stats", "generate_findings")
    graph.add_edge("generate_findings", END)
    return graph.compile()


def discovery_router(
    state: DiscoverySingleSourceInputState,
) -> Literal["generate_stats", "generate_findings"]:
    """
    Route the discovery agent to the appropriate node.
    """

    match state.get("next_discovery_action"):
        case "generate_stats":
            return "generate_stats"
        case "generate_findings":
            return "generate_findings"
        case _:
            raise ValueError("__end__")
