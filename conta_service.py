from datetime import datetime
from decimal import Decimal

from models.cliente import Cliente
from models.conta import Conta
from models.conta_repository import ContaRepository
from models.movimentacao import Movimentacao


class ContaService:
    """Centraliza e protege as regras de negocio bancarias."""

    def __init__(self, repository: ContaRepository) -> None:
        self.repository = repository

    def criar_conta(self, nome: str, cpf: str, saldo_inicial: Decimal) -> Conta:
        saldo = Decimal(str(saldo_inicial))
        if saldo < 0:
            raise ValueError("O saldo inicial nao pode ser negativo.")
        conta = Conta(self.repository.proximo_numero(), Cliente(nome, cpf), saldo)
        if saldo > 0:
            conta.historico.append(Movimentacao("ABERTURA", saldo, datetime.now()))
        self.repository.salvar(conta)
        return conta

    def depositar(self, numero: int, valor: Decimal) -> Conta:
        conta = self._obter_conta(numero)
        quantia = self._validar_valor(valor)
        conta.saldo += quantia
        conta.historico.append(Movimentacao("DEPOSITO", quantia, datetime.now()))
        self.repository.salvar(conta)
        return conta

    def sacar(self, numero: int, valor: Decimal) -> Conta:
        conta = self._obter_conta(numero)
        quantia = self._validar_valor(valor)
        if quantia > conta.saldo:
            raise ValueError("Saldo insuficiente.")
        conta.saldo -= quantia
        conta.historico.append(Movimentacao("SAQUE", quantia, datetime.now()))
        self.repository.salvar(conta)
        return conta

    def consultar(self, numero: int) -> Conta:
        return self._obter_conta(numero)

    def _obter_conta(self, numero: int) -> Conta:
        conta = self.repository.buscar(numero)
        if conta is None:
            raise ValueError("Conta nao encontrada.")
        return conta

    @staticmethod
    def _validar_valor(valor: Decimal) -> Decimal:
        quantia = Decimal(str(valor))
        if quantia <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return quantia
