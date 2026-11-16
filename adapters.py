from dataclasses import dataclass, field
from typing import Literal, Protocol
from app.contracts import Signal

@dataclass
class AdapterResult:
    adapter_name: str
    state: Literal["completed", "partial", "not_configured", "failed"]
    signals: list[Signal] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)

class MediaAdapter(Protocol):
    async def analyze(self, media_ref: str) -> AdapterResult: ...

class UnconfiguredAdapter:
    """Explicit placeholder; never invents a detection or pass result."""
    def __init__(self, name: str, signal_kinds: list[str]):
        self.name, self.signal_kinds = name, signal_kinds

    async def analyze(self, media_ref: str) -> AdapterResult:
        return AdapterResult(
            adapter_name=self.name,
            state="not_configured",
            signals=[Signal(signal_id=f"{self.name}:{kind}", kind=kind,
                            status="not_run",
                            limitations=[f"{self.name} adapter is not connected."])
                     for kind in self.signal_kinds],
            limitations=[f"{self.name} analysis has not been performed."]
        )
