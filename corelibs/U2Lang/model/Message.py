from dataclasses import dataclass, field

@dataclass
class Message:
    data: dict
    metadata: dict = field(default_factory=dict)