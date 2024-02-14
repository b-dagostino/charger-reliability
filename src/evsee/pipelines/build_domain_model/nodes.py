"""
This is a boilerplate pipeline 'build_domain_model'
generated using Kedro 0.19.2
"""

import pandas as pd


def find_unique_stations(*inputs: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Find unique stations (according to station MAC address) across all data
    (i.e., station overview, station inventory, alarms, charging sessions).

    Returns:
        pd.DataFrame: Dataframe containing all unique station MAC address.
    """

    # Get unique stations from all tables
    mac_columns: list[pd.DataFrame] = [
        input["MAC Address"].to_frame()
        for input in inputs
        if "MAC Address" in input.columns
    ]

    unique_stations: pd.DataFrame = (
        pd.concat(mac_columns)
        .sort_values("MAC Address")
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return unique_stations
