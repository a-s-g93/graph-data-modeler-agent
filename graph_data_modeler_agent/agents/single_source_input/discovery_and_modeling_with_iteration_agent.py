from instructor import AsyncInstructor
from langgraph.graph import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph

from ...components.state import (
    SingleSourceInputState,
    SingleSourceMainState,
    SingleSourceOutputState,
)
from .discovery_agent import create_discovery_agent
from .modeling_agent import create_data_modeler_agent
from .modeling_update_agent import create_data_modeler_update_agent


def create_discovery_and_modeling_with_iteration_agent(
    discovery_llm_client: AsyncInstructor,
    modeling_llm_client: AsyncInstructor,
    discovery_model: str,
    modeling_model: str,
) -> CompiledStateGraph:
    """
    Create a discovery and modeling agent that will generate a graph data model from a single source.
    """

    graph = StateGraph(
        input=SingleSourceInputState,
        state_schema=SingleSourceMainState,
        output=SingleSourceOutputState,
    )

    graph.add_node(
        "discovery_agent",
        create_discovery_agent(discovery_llm_client, discovery_model),
    )

    graph.add_node(
        "data_modeler_agent",
        create_data_modeler_agent(modeling_llm_client, modeling_model),
    )

    graph.add_node(
        "data_modeler_update_agent",
        create_data_modeler_update_agent(modeling_llm_client, modeling_model),
    )

    graph.add_edge(START, "discovery_agent")
    graph.add_edge("discovery_agent", "data_modeler_agent")
    graph.add_conditional_edges("data_modeler_agent", no_model_router, {"data_modeler_update_agent": "data_modeler_update_agent"})
    graph.add_edge("data_modeler_update_agent", END)

    return graph.compile()


def no_model_router(state: SingleSourceMainState) -> str:
    """
    Route the state to the appropriate node.
    """

    if state.get("data_model", None) is None or not state["data_model"].nodes:
        return END
    else:
        return "data_modeler_update_agent"
