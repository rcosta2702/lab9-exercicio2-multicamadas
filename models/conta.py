from dataclasses import dataclass, field
from decimal import Decimal

from models.cliente import Cliente
from models.movimentacao import Movimentacao


@dataclass
class Conta:
    numero: int
    cliente: Cliente
    saldo: Decimal = Decimal("0")
    historico: list[Movimentacao] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.saldo = Decimal(str(self.saldo))
