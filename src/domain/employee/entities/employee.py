from dataclasses import dataclass
from ..value_objects.work_regime import WorkRegime
from ..value_objects.contract_type import Contract


@dataclass
class Employee:
    name: str
    work_regime: WorkRegime
    contract: Contract
    