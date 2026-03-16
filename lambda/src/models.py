from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class ClassificationResult:
    category: str
    priority: str
    team: str
    confidence: float
    suggested_response: str
    model_source: str

    def to_dict(self) -> Dict:
        return asdict(self)
