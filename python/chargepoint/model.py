from enum import Enum, auto

from statemachine import StateMachine
from statemachine.states import States


class NetworkStatus(Enum):
    """Network connectivity states"""
    UNKNOWN = auto()
    REACHABLE = auto()
    UNREACHABLE = auto()


class NetworkStatusMachine(StateMachine):
    "Network connectivity state machine"
    states = States.from_enum(NetworkStatus, NetworkStatus.UNKNOWN)

    test = states.UNKNOWN.to(states.REACHABLE) | states.REACHABLE.to(states.UNREACHABLE) | states.UNREACHABLE.to(states.UNKNOWN)