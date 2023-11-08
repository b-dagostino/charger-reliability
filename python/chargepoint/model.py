from enum import Enum
from typing import Any, NamedTuple

from statemachine import State
from statemachine.transition_list import TransitionList

from .alarms import AlarmEnum
from .state_machine import HistoricalStateMachine


class NetworkStatus(HistoricalStateMachine):
    """Network status state machine"""

    unknown: State = State(initial=True)
    reachable: State = State()
    unreachable: State = State()

    alarms_to_transitions_map: dict[AlarmEnum, TransitionList] = {
        AlarmEnum.UNREACHABLE: unreachable.from_(unknown, reachable, unreachable),
        AlarmEnum.POWERED_OFF: unreachable.from_(unknown, reachable, unreachable),
    }

    for alarm in AlarmEnum:
        if alarm not in [AlarmEnum.UNREACHABLE, AlarmEnum.POWERED_OFF]:
            alarms_to_transitions_map[alarm] = reachable.from_(unknown, reachable, unreachable)


class StationStatus(HistoricalStateMachine):
    """Station status state machine"""

    def __init__(
        self,
        model: Any = None,
        state_field: str = "state",
        start_value: Any = None,
        rtc: bool = True,
        allow_event_without_transition: bool = False,
        return_to_last_known_state: bool = False,
    ):
        super().__init__(model, state_field, start_value, rtc, allow_event_without_transition)
        self._return_to_last_known_state = return_to_last_known_state

    unknown: State = State(initial=True)
    available: State = State()
    occupied: State = State()
    unavailable: State = State()
    unreachable: State = State()
    faulted: State = State()

    alarms_to_transitions_map: dict[AlarmEnum, TransitionList] = {}

    # Boot alarms always transition to available
    for boot_alarm in AlarmEnum.boot:
        alarms_to_transitions_map[boot_alarm] = available.from_(
            unknown, available, occupied, unavailable, unreachable, faulted
        )

    # Fault alarms always tranistion to faulted
    for fault_alarm in AlarmEnum.faults:
        alarms_to_transitions_map[fault_alarm] = faulted.from_(unknown, available, occupied, unavailable, unreachable, faulted)

    # Fault cleared alarm transitions to available
    alarms_to_transitions_map[AlarmEnum.FAULT_CLEARED] = available.from_(
        unknown, available, unavailable, unreachable, faulted
    )

    # Network status alarms
    alarms_to_transitions_map.update(
        {
            # Unreachable alarms always transition to unreachable
            AlarmEnum.UNREACHABLE: unreachable.from_(unknown, available, unavailable, occupied, unreachable, faulted),
            # Reachable alarms transition to last known state (if enabled), otherwise return to available
            AlarmEnum.REACHABLE: unreachable.to(available, occupied, unavailable, faulted, cond="reachable_guard")
            | unreachable.to(available),
        }
    )

    # Power off alarms transition to unavailable
    alarms_to_transitions_map[AlarmEnum.POWERED_OFF] = unavailable.from_(
        unknown, available, occupied, unavailable, unreachable, faulted
    )

    # All other alarms essentially indicate the station is available
    for alarm in AlarmEnum:
        if alarm not in list(alarms_to_transitions_map.keys()):
            alarms_to_transitions_map[alarm] = available.from_(unknown, available, unavailable, unreachable, faulted)

    def reachable_guard(self, event_data):
        if not self._return_to_last_known_state:
            return False
        last_known_state = next(
            (
                x.state
                for x in reversed(self.history.entries)
                if x.state != __class__.unknown and x.state != __class__.unreachable
            ),
            None,
        )
        if last_known_state == event_data.target:
            return True
        else:
            return False


class CircuitSharingStatus(HistoricalStateMachine):
    """Circuit sharing status state machine"""

    def __init__(
        self,
        model: Any = None,
        state_field: str = "state",
        start_value: Any = None,
        rtc: bool = True,
        allow_event_without_transition: bool = False,
        return_to_last_known_state: bool = False,
    ):
        super().__init__(model, state_field, start_value, rtc, allow_event_without_transition)
        self._return_to_last_known_state = return_to_last_known_state

    unknown: State = State(initial=True)
    unreachable: State = State()
    reduced: State = State()
    restored: State = State()

    alarms_to_transitions_map: dict[AlarmEnum, TransitionList] = {
        AlarmEnum.CIRCUIT_SHARING_REDUCED: reduced.from_(unknown, reduced, restored),
        AlarmEnum.CIRCUIT_SHARING_RESTORED: restored.from_(unknown, reduced, restored),
        AlarmEnum.UNREACHABLE: unreachable.from_(unknown, reduced, restored),
        AlarmEnum.REACHABLE: unreachable.to(reduced, restored, cond="reachable_guard") | unreachable.to(unknown),
        AlarmEnum.POWERED_OFF: unreachable.from_(unknown, reduced, restored),
    }

    for boot_alarm in AlarmEnum.boot:
        alarms_to_transitions_map[boot_alarm] = unknown.from_(unreachable, reduced, restored)

    def reachable_guard(self, event_data):
        if not self._return_to_last_known_state:
            return False
        last_known_state = next(
            (
                x.state
                for x in reversed(self.history.entries)
                if x.state != __class__.unknown and x.state != __class__.unreachable
            ),
            None,
        )
        if last_known_state == event_data.target:
            return True
        else:
            return False


class ChargerModel:
    class ChargerState(NamedTuple):
        network_status: NetworkStatus
        station_status: StationStatus
        current_sharing_status: CircuitSharingStatus

    def __init__(self, return_to_last_known_state: bool = False) -> None:
        self._state = __class__.ChargerState(
            network_status=NetworkStatus(),
            station_status=StationStatus(return_to_last_known_state=return_to_last_known_state),
            current_sharing_status=CircuitSharingStatus(return_to_last_known_state=return_to_last_known_state),
        )

    @property
    def state(self):
        return self._state

    def send(self, event: str | Enum):
        for state in self.state:
            state.send(event)

    def __repr__(self) -> str:
        state_string = ", ".join([f"{k}={v.current_state.name}" for k, v in self.state._asdict().items()])
        return f"{self.__class__.__name__}({state_string})"
