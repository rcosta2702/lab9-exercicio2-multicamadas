from models.conta import Conta


class ContaRepository:
    def __init__(self) -> None:
        self._contas: dict[int, Conta] = {}

    def salvar(self, conta: Conta) -> None:
        self._contas[conta.numero] = conta

    def buscar(self, numero: int) -> Conta | None:
        return self._contas.get(numero)

    def proximo_numero(self) -> int:
        return max(self._contas, default=0) + 1
