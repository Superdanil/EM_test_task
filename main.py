import getpass

from service import WalletService


def greetings(name: str) -> None:
    """Функция приветствия пользователя."""
    print(f"Добро пожаловать в личный кошелек, {name}. \n"
          f"Введите ваш запрос, после чего, нажмите Enter. Для выхода из программы нажмите Enter.")


def run() -> None:
    """Функция запуска клиента."""
    service = WalletService()
    while True:
        request = input()
        if len(request) == 0:
            print("Goodbye!")
            break
        else:
            service(request)


if __name__ == "__main__":
    greetings(getpass.getuser())
    run()
