"""
This is a boilerplate pipeline 'charger_model'
generated using Kedro 0.19.2
"""

import pandas as pd
from chargepoint import AlarmEnum, ChargerModel


def predict_charger_state(
    unique_stations: pd.DataFrame, alarms: pd.DataFrame
) -> pd.DataFrame:
    """
    Build historical charger states using unique stations and alarms.

    Args:
        unique_stations (pd.DataFrame): _description_
        alarms (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: Historical charger states
    """
    # Mapping from MAC addresses to models. Each MAC address corresponds to one unique charger model.
    models: dict[str, ChargerModel] = {}

    # Create charger models
    for mac_address in unique_stations["MAC Address"]:
        models[mac_address] = ChargerModel(return_to_last_known_state=False)

    charger_states = {"MAC Address": [], "Time": [], "State": []}

    # Iterate through all alarms chronologically and send to underlying charger state models.
    for index, row in alarms.iterrows():
        mac_address = row["MAC Address"]
        model = models[mac_address]

        alarm = AlarmEnum(row["Alarm Name"])
        model.send(alarm)

        charger_states["MAC Address"].append(mac_address)
        charger_states["Time"].append(row["Alarm Time"])
        charger_states["State"].append(model.state.station_status.current_state.name)

    charger_states = pd.DataFrame(data=charger_states)

    return charger_states


def charger_state_history(charger_states: pd.DataFrame) -> pd.DataFrame():
    states = []
    indices = []

    for mac, group in charger_states.groupby("MAC Address"):
        group["Interval"] = (group.State != group.State.shift()).cumsum()
        group = group.groupby("Interval").last().drop(columns=["MAC Address"])

        for index, row in group.iterrows():
            if not index + 1 in group.index:
                break
            state = row.State
            start = row.Time
            end = group.loc[index + 1, "Time"]
            interval = pd.Interval(left=start, right=end, closed="left")
            states.append(state)
            indices.append((mac, interval))

    index = pd.MultiIndex.from_tuples(indices, names=["MAC Address", "Interval"])
    charger_state_history = pd.Series(states, index=index, name="State").to_frame()
    charger_state_history["Duration"] = (
        charger_state_history["State"]
        .index.to_frame()["Interval"]
        .map(lambda x: x.length)
    )

    return charger_state_history


def charger_stats(charger_state_history):
    state_summary = charger_state_history.pivot_table(
        columns="State", index="MAC Address", values="Duration", aggfunc="sum"
    ).fillna(pd.Timedelta(seconds=0))
    state_summary["Total"] = state_summary.sum(axis=1)

    state_summary_normalized = state_summary.divide(
        state_summary["Total"], axis=0
    ).drop(columns=["Total"])

    spearman_correlation = state_summary.corr("spearman")

    return (state_summary, state_summary_normalized, spearman_correlation)
