from controllers.conta_controller import ContaController
from models.conta_repository import ContaRepository
from conta_service import ContaService
from views.conta_view import ContaView


def main() -> None:
    repository = ContaRepository()
    ContaController(ContaService(repository), ContaView()).executar()


if __name__ == "__main__":
    main()
