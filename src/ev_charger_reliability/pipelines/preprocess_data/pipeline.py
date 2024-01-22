"""
This is a boilerplate pipeline 'preprocess_data'
generated using Kedro 0.19.1
"""

from kedro.pipeline import node, Pipeline, pipeline

from .nodes import preprocess_station_inventory, preprocess_stations_overview, preprocess_alarms


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                preprocess_station_inventory,
                inputs="station_inventory",
                outputs="preprocessed_station_inventory",
                name="preprocess_station_inventory",
            ),
            node(
                preprocess_stations_overview,
                inputs="stations_overview",
                outputs="preprocessed_stations_overview",
                name="preprocess_stations_overview"
            ),
            node(
                preprocess_alarms,
                inputs="alarms",
                outputs="preprocessed_alarms",
                name="preprocess_alarms"
            )
        ]
    )
