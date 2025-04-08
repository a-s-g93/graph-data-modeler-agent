from typing import Literal

from instructor import AsyncInstructor
from langgraph.constants import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph

from ...components.data_modeler import (
    create_data_modeler_error_handler_node,
    create_generate_data_model_single_source_node,
    create_generate_nodes_single_source_node,
)
from ...components.data_modeler.state import (
    DataModelerSingleSourceInputState,
    DataModelerSingleSourceMainState,
    DataModelerSingleSourceOutputState,
)


def create_data_modeler_agent(
    llm_client: AsyncInstructor, model: str
) -> CompiledStateGraph:
    """
    Create a discovery agent that will generate a graph data model from a single source.
    """

    graph = StateGraph(
        input=DataModelerSingleSourceInputState,
        state_schema=DataModelerSingleSourceMainState,
        output=DataModelerSingleSourceOutputState,
    )

    generate_nodes = create_generate_nodes_single_source_node(
        llm_client=llm_client, model=model
    )
    generate_data_model = create_generate_data_model_single_source_node(
        llm_client=llm_client, model=model
    )
    data_modeler_error_handler = create_data_modeler_error_handler_node()

    graph.add_node("generate_nodes", generate_nodes)
    graph.add_node("generate_data_model", generate_data_model)
    graph.add_node("data_modeler_error_handler", data_modeler_error_handler)
    graph.add_edge(START, "generate_nodes")
    graph.add_conditional_edges(
        "generate_nodes",
        data_modeler_router,
        {
            "generate_data_model": "generate_data_model",
            "data_modeler_error_handler": "data_modeler_error_handler",
        },
    )
    graph.add_conditional_edges(
        "generate_data_model",
        data_modeler_router,
        {"__end__": END, "data_modeler_error_handler": "data_modeler_error_handler"},
    )
    graph.add_edge("data_modeler_error_handler", END)
    return graph.compile()


def data_modeler_router(
    state: DataModelerSingleSourceMainState,
) -> Literal["data_modeler_error_handler", "generate_data_model", "__end__"]:
    """
    Route the data modeler agent to the appropriate node.
    """
    match state.get("next_data_modeler_action"):
        case "generate_data_model":
            return "generate_data_model"
        case "data_modeler_error_handler":
            return "data_modeler_error_handler"
        case "__end__":
            return "__end__"
        case _:
            raise ValueError("data_modeler_error_handler")
