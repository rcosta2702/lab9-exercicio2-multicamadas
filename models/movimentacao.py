from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Movimentacao:
    tipo: str
    valor: Decimal
    data_hora: datetime

    def __str__(self) -> str:
        data = self.data_hora.strftime("%d/%m/%Y %H:%M:%S")
        return f"{data} | {self.tipo:<9} | R$ {self.valor:.2f}"
