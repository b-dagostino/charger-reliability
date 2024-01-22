"""
Data preprocessing pipeline for basic table cleaning, merging, and typing.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def preprocess_station_inventory(station_inventory: pd.DataFrame) -> pd.DataFrame:
    """Clean up and type raw station inventory

    Args:
        station_inventory (pd.DataFrame): Raw station inventory

    Returns:
        pd.DataFrame: Cleaned and typed station inventory
    """

    # Drop NaN columns
    station_inventory.dropna(axis=1, how="all", inplace=True)

    # Sanitize column names
    station_inventory.rename(columns=str.strip, inplace=True)

    # Drop unneeded columns
    station_inventory.drop(
        labels=[
            "Org Name",
            "Org ID",
            "Hardware S/N",
            "Extended Warranty S/N",
            "Warranty Description",
            "Token S/N",
            "Cloud Plan",
            "Activation Date (Pacific Time)",
            "Expiration Date (Pacific Time)",
            "Customer Name",
            "Customer ID",
        ],
        axis=1,
        inplace=True,
    )

    # Convert column types
    station_inventory = station_inventory.astype(
        {
            "EVSE ID": "int64",  # Unique non-negative integers
            "Station Name": "string",  # Unique, non-empty strings
            "Model Number": "category",  # Several stations share the same model number
            "MAC Address": "string",  # Unique, non-empty strings
            "Address": "category",  # Several stations share the same address
        }
    )

    # Issue warning if any rows contain NaNs
    if station_inventory.isna().any(axis=None):
        logger.warn("'preprocessed_station_inventory' contains missing values")

    return station_inventory


def preprocess_stations_overview(stations_overview: pd.DataFrame) -> pd.DataFrame:
    """Clean up and type raw stations overview

    Args:
        stations_overview (pd.DataFrame): Raw stations overview

    Returns:
        pd.DataFrame: Cleaned and typed stations overview
    """

    # Drop NaN columns
    stations_overview.dropna(axis=1, how="all", inplace=True)

    # Sanitize column names
    stations_overview.rename(columns=str.strip, inplace=True)

    # Drop unneeded columns
    stations_overview.drop(
        labels=[
            "Org Name",
            "Pricing Policy Name",
            "Reservations",
            "Station Message",
            "Enabled",
            "Station Activation Type",
            "Usable By",
            "Visibility (Access Policy Name)",
            "Customer Category",
            "Customer Subcategory",
            "Currency Name",
            "Device Access Restriction",
            "Asset Tag ID",
            "Meter ID",
            "Customer Name",
            "Customer ID",
            "Paired",
        ],
        axis=1,
        inplace=True,
    )

    # Convert column types
    stations_overview = stations_overview.astype(
        {
            "Model Number": "category",
            "Station Name": "string",
            "MAC Address": "string",
            "Address 1": "category",
            "Address 2": "category",
            "Floor Label": "category",
            "City": "category",
            "State": "category",
            "Zip/Postal Code": "category",
            "County": "category",
            "Country": "category",
            "Activation Status": "category",
            "Network Status": "category",
            "Station Status": "category",
            "Port 1 Status": "category",
            "Port 2 Status": "category",
            "No. of Ports": "int64",
            "EVSE ID": "int64",
            "Radio Group Name": "category",
            "Software Version": "category",
            "Circuit Sharing": "category",
            "Power Select / AC Breaker Rating": "category",
            "Warranty": "category",
            "Warranty Service": "category",
            "Plug Type": "category",
            "Site Validation Status": "category",
            "Latitude": "float64",
            "Longitude": "float64",
        }
    )
    stations_overview["Station Activation Date"] = pd.to_datetime(
        stations_overview["Station Activation Date"]
    )
    stations_overview["Warranty Expiration Date"] = pd.to_datetime(
        stations_overview["Warranty Expiration Date"]
    )

    return stations_overview


def preprocess_alarms(alarms: pd.DataFrame) -> pd.DataFrame:
    """Clean up and type raw alarms

    Args:
        alarms (pd.DataFrame): Raw alarms

    Returns:
        pd.DataFrame: Cleaned and typed alarms
    """

    # Drop NaN columns
    alarms.dropna(axis=1, how="all", inplace=True)

    # Sanitize column names
    alarms.rename(columns=str.strip, inplace=True)

    # Drop unneeded columns
    alarms.drop(
        labels=["Org Name", "Reason For Clearing"],
        axis=1,
        inplace=True,
    )

    # Convert column types
    alarms = alarms.astype(
        {
            "Display Name": "category",
            "MAC Address": "category",
            "Alarm Name": "category",
            "Alarm ID": "category",
            "Model Number": "category",
            "Port": "category",
        }
    )

    # Convert alarm time column to timezone-aware datetime
    dst_bool = alarms["Alarm Time"].str.contains("ST")

    alarms["Alarm Time"] = pd.to_datetime(
        alarms["Alarm Time"].str.split().str[:-1].str.join(" ")
    ).dt.tz_localize("US/Pacific", ambiguous=dst_bool)

    return alarms


# def preprocess_charging_sessions(chargin):
#     pass
