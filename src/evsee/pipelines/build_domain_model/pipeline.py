"""
This is a boilerplate pipeline 'build_domain_model'
generated using Kedro 0.19.2
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import find_unique_stations


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                find_unique_stations,
                inputs=[
                    "stations_overview_typed",
                    "station_inventory_typed",
                    "alarms_typed",
                    "charging_sessions_typed",
                ],
                outputs="stations_primary",
                name="find_unique_stations",
            )
        ]
    )
