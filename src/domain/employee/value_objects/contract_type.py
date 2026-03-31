from __future__ import annotations
from enum import Enum
from dataclasses import dataclass


class ContractType(str, Enum):
    CLT = "clt"
    PJ = "pj"
    JA = "jovem aprendiz"


@dataclass(frozen=True)
class Contract:
    contract: ContractType

    @classmethod
    def from_string(cls, value: str) -> Contract:
        try:
            return cls(contract=ContractType(value.lower()))
        
        except ValueError:
            valid_values = [c.value for c in ContractType]

            raise ValueError(
                f"Contrato '{value}' inválido. "
                f"Valores aceitos: {valid_values}"
            )
        
    def __str__(self) -> str:
        return self.contract.value
