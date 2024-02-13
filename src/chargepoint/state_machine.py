from abc import ABC
from enum import Enum
from sys import stderr
from typing import Any, NamedTuple, Optional

import pandas as pd
import statemachine
import statemachine.factory
from statemachine import State
from statemachine.event import TransitionNotAllowed
from statemachine.transition_list import TransitionList


class StateMachineMetaClass(statemachine.factory.StateMachineMetaclass, ABC):
    def add_from_attributes(cls, attrs):
        # Add events for dictionary attributes that map from enum instances to TransitionList
        for _, value in sorted(attrs.items(), key=lambda pair: pair[0]):
            if isinstance(value, dict):
                for k, v in value.items():
                    if not isinstance(v, TransitionList):
                        continue
                    if isinstance(k, Enum):
                        cls.add_event(str(k), v)

        # Defer to python-statemachine metaclass to add events from remaining attributes
        super().add_from_attributes(attrs)


class StateMachine(statemachine.StateMachine, metaclass=StateMachineMetaClass):
    """State machine class that additionally accepts enums as events"""

    def send(self, event: str | Enum, *args, **kwargs):
        event = str(event) if isinstance(event, Enum) else event
        try:
            return super().send(event, *args, **kwargs)
        except TransitionNotAllowed as e:
            pass
            # print(f"{self}: No transition for {e.event} from {e.state}", file=stderr)


class HistoricalStateMachine(StateMachine):
    """State machine that keeps track of its own history"""

    class StateMachineHistory:
        class StateHistoryEntry(NamedTuple):
            event: Any
            state: State
            timestamp: Any

        def _append(self, event, state, timestamp=None):
            self._entries.append(__class__.StateHistoryEntry(event, state, timestamp))

        def __init__(self, sm: Optional[StateMachine] = None) -> None:
            self._entries: list[__class__.StateHistoryEntry] = []
            if sm is not None:
                self._append(None, sm.current_state)

        def to_dataframe(self):
            return pd.DataFrame(map(lambda x: x._asdict(), self._entries))

        @property
        def entries(self) -> tuple[StateHistoryEntry, ...]:
            return tuple(self._entries)

        def __getitem__(self, key):
            return self._entries[key]

        def __iter__(self):
            return iter(self._entries)

    def __init__(
        self,
        model: Any = None,
        state_field: str = "state",
        start_value: Any = None,
        rtc: bool = True,
        allow_event_without_transition: bool = False,
    ):
        super().__init__(
            model, state_field, start_value, rtc, allow_event_without_transition
        )
        self._history = __class__.StateMachineHistory(self)

    def after_transition(self, event, state):
        self.history._append(event, state)

    @property
    def history(self):
        return self._history
