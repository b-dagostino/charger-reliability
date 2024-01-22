"""
This is a boilerplate pipeline 'preprocess_data'
generated using Kedro 0.19.1
"""

from kedro.pipeline import node, Pipeline, pipeline

from .nodes import (
    preprocess_station_inventory,
    preprocess_stations_overview,
    preprocess_alarms,
    preprocess_charging_sessions,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                preprocess_station_inventory,
                inputs="station_inventory_raw",
                outputs="station_inventory_preprocessed",
                name="preprocess_station_inventory",
            ),
            node(
                preprocess_stations_overview,
                inputs="stations_overview_raw",
                outputs="stations_overview_preprocessed",
                name="preprocess_stations_overview",
            ),
            node(
                preprocess_alarms,
                inputs="alarms_raw",
                outputs="alarms_preprocessed",
                name="preprocess_alarms",
            ),
            node(
                preprocess_charging_sessions,
                inputs="charging_sessions_raw",
                outputs="charging_sessions_preprocessed",
                name="preprocess_charging_sessions",
            ),
        ]
    )
