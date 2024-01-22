"""
Data preprocessing pipeline for basic table cleaning, merging, and typing.
"""

import logging
from typing import Any, Callable, Dict

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
            "Address": "category",  # Several stations share the same address,
            "Hardware S/N": "int64"
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

    # Sort by alarm time

    return alarms


def preprocess_charging_sessions(
    charging_sessions: Dict[str, Callable[[], Any]]
) -> pd.DataFrame:
    """Concatenate, clean, and type raw charging sessions

    Args:
        charging_sessions (Dict[str, Callable[[], Any]]): Partioned raw charging sessions

    Returns:
        pd.DataFrame: Concatenated, cleaned, and typed charging sessions
    """

    # Concatenate charging sessions
    charging_sessions: pd.DataFrame = pd.concat(
        [f() for f in charging_sessions.values()], ignore_index=True
    )

    # Drop NaN columns
    charging_sessions.dropna(axis=1, how="all", inplace=True)

    # Sanitize column names
    charging_sessions.rename(columns=str.strip, inplace=True)

    # Start and end times
    charging_sessions["Start Time"] = pd.to_datetime(
        charging_sessions["Start Date"], format="mixed"
    ).dt.tz_localize(
        "US/Pacific", ambiguous=charging_sessions["Start Time Zone"].str.contains("ST")
    )

    charging_sessions["End Time"] = pd.to_datetime(
        charging_sessions["End Date"], format="mixed"
    ).dt.tz_localize(
        "US/Pacific", ambiguous=charging_sessions["End Time Zone"].str.contains("ST")
    )

    # Drop unneeded columns
    charging_sessions.drop(
        labels=[
            "Org Name",
            "Transaction Date (Pacific Time)",
            "Start Date",
            "Start Time Zone",
            "End Date",
            "End Time Zone",
        ],
        axis=1,
        inplace=True,
    )

    # Convert column types
    charging_sessions = charging_sessions.astype(
        {
            "Station Name": "category",
            "MAC Address": "category",
            "Energy (kWh)": "float64",
            "GHG Savings (kg)": "float64",
            "Gasoline Savings (gallons)": "float64",
            "Port Type": "category",
            "Plug Type": "category",
            "EVSE ID": "category",
            "Address 1": "category",
            "Address 2": "category",
            "City": "category",
            "State/Province": "category",
            "Zip/Postal Code": "category",
            "Country": "category",
            "Latitude": "float64",
            "Longitude": "float64",
            "Currency": "category",
            "Fee": "float64",
            "Ended By": "category",
            "Plug In Event ID": "int64",
            "Transaction ID": "int64",
            "Driver Zip/Postal Code": "category",
            "User ID": "str",
            "County": "category",
            "System S/N": "int64",
            "Model Number": "category"
        }
    )
    charging_sessions["Port Number"] = (
        charging_sessions["Port Number"].astype("str").astype("category")
    )
    charging_sessions["Total Duration (hh:mm:ss)"] = pd.to_timedelta(
        charging_sessions["Total Duration (hh:mm:ss)"]
    )
    charging_sessions["Charging Time (hh:mm:ss)"] = pd.to_timedelta(
        charging_sessions["Charging Time (hh:mm:ss)"]
    )
    charging_sessions["Start SOC"] = (
        charging_sessions["Start SOC"]
        .str.replace("%", "")
        .astype("float")
        .astype("category")
    )
    charging_sessions["End SOC"] = (
        charging_sessions["End SOC"]
        .str.replace("%", "")
        .astype("float")
        .astype("category")
    )

    return charging_sessions
