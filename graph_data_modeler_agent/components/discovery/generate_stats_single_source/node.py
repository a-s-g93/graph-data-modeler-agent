import io
from typing import Any, Callable, Coroutine

import pandas as pd
from numpy import number

from graph_data_modeler_agent.components.discovery.models import PandasStatsResponse

from ..state import DiscoverySingleSourceMainState


def create_generate_stats_single_source_node() -> (
    Callable[[DiscoverySingleSourceMainState], Coroutine[Any, Any, dict[str, Any]]]
):
    """
    Create the generate stats node.
    """

    async def generate_stats_single_source(
        state: DiscoverySingleSourceMainState,
    ) -> dict[str, Any]:
        """
        Generate the stats for the data to inform the discovery process.
        """

        errors = list()

        df = state["data"]
        buffer = io.StringIO()
        df.info(buf=buffer, memory_usage=False, verbose=True)

        df_info = buffer.getvalue()
        try:
            desc_numeric = df.describe(
                percentiles=[0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99],
                include=[number],
            )
        except ValueError as e:
            errors.append(str(e))
            desc_numeric = pd.DataFrame()
        try:
            desc_categorical = df.describe(include="object")
        except ValueError as e:
            errors.append(str(e))
            desc_categorical = pd.DataFrame()

        return {
            "stats": PandasStatsResponse(
                categorical_description=desc_categorical,
                general_description=df_info,
                numerical_description=desc_numeric,
            ),
            "discovery_steps": ["generate_stats"],
            "errors": errors,
        }

    return generate_stats_single_source
