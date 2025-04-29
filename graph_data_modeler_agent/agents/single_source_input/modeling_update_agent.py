from typing import Literal

from instructor import AsyncInstructor
from langgraph.constants import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph

from ...components.data_model_updater import (
    create_update_data_model_single_source_node,
    create_brainstorm_updates_single_source_node,
)
from ...components.data_model_updater.state import (
    DataModelUpdaterSingleSourceInputState,
    DataModelUpdaterSingleSourceMainState,
    DataModelUpdaterSingleSourceOutputState,
)


def create_data_modeler_update_agent(
    llm_client: AsyncInstructor, model: str
) -> CompiledStateGraph:
    """
    Create a data modeler update agent that will update a graph data model from a single source.
    """

    graph = StateGraph(
        input=DataModelUpdaterSingleSourceInputState,
        state_schema=DataModelUpdaterSingleSourceMainState,
        output=DataModelUpdaterSingleSourceOutputState,
    )

    brainstorm_updates_node = create_brainstorm_updates_single_source_node(
        llm_client=llm_client, model=model
    )
    update_data_model = create_update_data_model_single_source_node(
        llm_client=llm_client, model=model
    )

    graph.add_node("brainstorm_updates", brainstorm_updates_node)
    graph.add_node("update_data_model", update_data_model)
    graph.add_edge(START, "brainstorm_updates")
    graph.add_edge("brainstorm_updates", "update_data_model")
    graph.add_edge("update_data_model", END)

    return graph.compile()


