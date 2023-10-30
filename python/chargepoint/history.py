from typing import NamedTuple


class IEntry:
    """An individual historical item"""

    pass


class IHistory:
    """An object with a history"""

    @property
    def history(self) -> tuple[NamedTuple, ...]:
        return ()
