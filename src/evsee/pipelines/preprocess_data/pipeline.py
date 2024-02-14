"""
This is a boilerplate pipeline 'preprocess_data'
generated using Kedro 0.19.1
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    preprocess_alarms,
    preprocess_charging_sessions,
    preprocess_station_inventory,
    preprocess_stations_overview,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                preprocess_station_inventory,
                inputs="station_inventory_raw",
                outputs="station_inventory_typed",
                name="preprocess_station_inventory",
            ),
            node(
                preprocess_stations_overview,
                inputs="stations_overview_raw",
                outputs="stations_overview_typed",
                name="preprocess_stations_overview",
            ),
            node(
                preprocess_alarms,
                inputs="alarms_raw",
                outputs="alarms_typed",
                name="preprocess_alarms",
            ),
            node(
                preprocess_charging_sessions,
                inputs="charging_sessions_raw",
                outputs="charging_sessions_typed",
                name="preprocess_charging_sessions",
            ),
        ]
    )