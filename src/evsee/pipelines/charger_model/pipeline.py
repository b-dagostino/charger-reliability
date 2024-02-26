"""
This is a boilerplate pipeline 'charger_model'
generated using Kedro 0.19.2
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import charger_state_history, charger_stats, predict_charger_state


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                predict_charger_state,
                inputs=["unique_stations", "alarms_typed"],
                outputs="charger_states",
                name="predict_charger_states",
            ),
            node(
                charger_state_history,
                inputs="charger_states",
                outputs="charger_history",
                name="build_charger_history",
            ),
            node(
                charger_stats,
                inputs="charger_history",
                outputs=[
                    "state_summary",
                    "state_summary_normalized",
                    "state_correlation",
                ],
                name="calculate_charger_stats",
            ),
        ]
    )
