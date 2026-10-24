from conta_service import ContaService
from views.conta_view import ContaView


class ContaController:
    def __init__(self, service: ContaService, view: ContaView) -> None:
        self.service = service
        self.view = view
        self.view.configurar_acoes(self._criar, self._depositar, self._sacar, self._consultar)

    def executar(self) -> None:
        self.view.iniciar()

    def _criar(self) -> None:
        self._executar(lambda: self.view.exibir_conta(self.service.criar_conta(*self.view.ler_cadastro())))

    def _depositar(self) -> None:
        self._executar(lambda: self.view.exibir_conta(self.service.depositar(self.view.ler_numero(), self.view.ler_decimal())))

    def _sacar(self) -> None:
        self._executar(lambda: self.view.exibir_conta(self.service.sacar(self.view.ler_numero(), self.view.ler_decimal())))

    def _consultar(self) -> None:
        self._executar(lambda: self.view.exibir_historico(self.service.consultar(self.view.ler_numero())))

    def _executar(self, acao) -> None:
        try:
            acao()
        except ValueError as exc:
            self.view.exibir_erro(str(exc))
