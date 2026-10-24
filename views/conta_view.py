import tkinter as tk
from decimal import Decimal, InvalidOperation
from tkinter import messagebox, ttk
from typing import Callable

from models.conta import Conta


class ContaView:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Exercicio 2 - Banco Multicamadas")
        self.root.geometry("720x600")

        principal = ttk.Frame(self.root, padding=20)
        principal.pack(fill="both", expand=True)
        ttk.Label(principal, text="Sistema bancario", font=("Segoe UI", 20, "bold")).pack(anchor="w")

        abas = ttk.Notebook(principal)
        abas.pack(fill="x", pady=15)
        cadastro = ttk.Frame(abas, padding=16)
        movimento = ttk.Frame(abas, padding=16)
        abas.add(cadastro, text="Criar conta")
        abas.add(movimento, text="Movimentar")

        self.nome = self._campo(cadastro, "Nome", 0)
        self.cpf = self._campo(cadastro, "CPF", 1)
        self.saldo_inicial = self._campo(cadastro, "Saldo inicial (R$)", 2)
        self.botao_criar = ttk.Button(cadastro, text="Criar conta")
        self.botao_criar.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        self.numero = self._campo(movimento, "Numero da conta", 0)
        self.valor = self._campo(movimento, "Valor (R$)", 1)
        botoes = ttk.Frame(movimento)
        botoes.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        self.botao_depositar = ttk.Button(botoes, text="Depositar")
        self.botao_sacar = ttk.Button(botoes, text="Sacar")
        self.botao_consultar = ttk.Button(botoes, text="Consultar / Historico")
        for botao in (self.botao_depositar, self.botao_sacar, self.botao_consultar):
            botao.pack(side="left", expand=True, fill="x", padx=4)

        self.resultado = tk.Text(principal, height=16, state="disabled", font=("Consolas", 10))
        self.resultado.pack(fill="both", expand=True)

    @staticmethod
    def _campo(pai: ttk.Frame, rotulo: str, linha: int) -> ttk.Entry:
        ttk.Label(pai, text=rotulo).grid(row=linha, column=0, sticky="w", padx=(0, 12), pady=5)
        entrada = ttk.Entry(pai, width=45)
        entrada.grid(row=linha, column=1, sticky="ew", pady=5)
        pai.columnconfigure(1, weight=1)
        return entrada

    def configurar_acoes(
        self,
        criar: Callable[[], None],
        depositar: Callable[[], None],
        sacar: Callable[[], None],
        consultar: Callable[[], None],
    ) -> None:
        self.botao_criar.configure(command=criar)
        self.botao_depositar.configure(command=depositar)
        self.botao_sacar.configure(command=sacar)
        self.botao_consultar.configure(command=consultar)

    def ler_cadastro(self) -> tuple[str, str, Decimal]:
        return self.nome.get().strip(), self.cpf.get().strip(), self._decimal(self.saldo_inicial.get())

    def ler_numero(self) -> int:
        try:
            return int(self.numero.get())
        except ValueError as exc:
            raise ValueError("Numero da conta invalido.") from exc

    def ler_decimal(self) -> Decimal:
        return self._decimal(self.valor.get())

    @staticmethod
    def _decimal(texto: str) -> Decimal:
        try:
            return Decimal(texto.replace(",", "."))
        except InvalidOperation as exc:
            raise ValueError("Valor invalido.") from exc

    def exibir_conta(self, conta: Conta) -> None:
        self._mostrar(f"Conta {conta.numero} | {conta.cliente.nome}\nSaldo: R$ {conta.saldo:.2f}")

    def exibir_historico(self, conta: Conta) -> None:
        linhas = [f"Conta {conta.numero} | {conta.cliente.nome}", f"Saldo: R$ {conta.saldo:.2f}", "", "Historico:"]
        linhas.extend(str(item) for item in conta.historico)
        if not conta.historico:
            linhas.append("Nenhuma movimentacao.")
        self._mostrar("\n".join(linhas))

    def _mostrar(self, texto: str) -> None:
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", texto)
        self.resultado.configure(state="disabled")

    def exibir_erro(self, mensagem: str) -> None:
        messagebox.showerror("Erro", mensagem, parent=self.root)

    def iniciar(self) -> None:
        self.root.mainloop()
