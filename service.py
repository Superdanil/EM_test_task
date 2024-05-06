from record_model import RecordModel
from repository import WalletRepository


class WalletService:
    def __init__(self):
        self.repository = WalletRepository()
        self.commands = {
            "баланс": self._get_balance,
            "история": self._get_records,
            "доход": self._add_record,
            "расход": self._add_record,
            "изменить": self._update_record,
            "удалить": self._delete_record,
        }

    def __call__(self, request: str) -> None:
        """Печатает результат обработки запроса."""
        request = request.lower()
        try:
            response = self._validate_request(request)
            if type(response) is str:
                print(response)
            elif type(response) is list:
                if len(response) > 0:
                    self._print_title()
                    for record in response:
                        print(record)
                else:
                    print("Пусто")
        except UserWarning as warning:
            print(warning)

    def _validate_request(self, request) -> list | str | None:
        """Метод валидации первого слова в запросе."""
        try:
            return self.commands[request.split()[0]](request)
        except KeyError:
            raise UserWarning("Неверный запрос, попробуй ещё раз по инструкции.")

    def _get_balance(self, *args) -> str:
        """Возвращает отформатированную строку с текущим балансом кошелька."""
        balance = self.repository.get_balance()['баланс']
        incomes = self.repository.get_balance()['доходы']
        expenses = self.repository.get_balance()['расходы']

        return f"Текущий баланс: 💵{balance}. Доходов на сумму 💵{incomes}, расходов на сумму 💵{expenses}."

    def _get_records(self, request: str) -> list[RecordModel]:
        """Возвращает список записей из кошелька по ключам."""
        if len(request.split()) < 2:
            return self.repository.get_records()
        elif request.split()[1] in ("доход", "доходов", "доходы"):
            return self.repository.get_records(category="доход")
        elif request.split()[1] in ("расход", "расходов", "расходы"):
            return self.repository.get_records(category="расход")
        elif request.split()[1].isdigit():
            return self.repository.get_records(value=int(request.split()[1]))
        elif "дата" in request.split()[1]:
            return self.repository.get_records(date=request.split()[1].split("=")[-1])
        else:
            return self.repository.get_records(description=request.split()[1])

    def _add_record(self, request: str) -> str:
        """Добавляет одну запись о доходах/расходах в кошелёк."""
        try:
            category, value, date, *description = request.split()
        except ValueError:
            raise UserWarning("Недостаточно аргументов для запроса.")
        description = " ".join(description)
        try:
            new_record = RecordModel(category=category, value=value, date=date, description=description)
        except ValueError as e:
            raise UserWarning(e)
        else:
            record = self.repository.add(record=new_record)
            return f"Запись добавлена: {record}"

    def _update_record(self, request: str) -> str:
        """Изменяет одну запись в кошельке по её id."""
        try:
            id, category, value, date, *description = request.split()[1::]
        except ValueError:
            raise UserWarning("Недостаточно аргументов для запроса.")
        description = " ".join(description)
        try:
            record = RecordModel(id=id, category=category, value=value, date=date, description=description)
            return f"Запись изменена на {self.repository.update(record)}"
        except ValueError as e:
            raise UserWarning(e)

    def _delete_record(self, request: str) -> str:
        """Удаляет одну запись о доходах/расходах из кошелька по id."""
        try:
            id = int(request.split()[1])
        except IndexError:
            raise UserWarning("Недостаточно аргументов для запроса.")
        except ValueError:
            raise UserWarning("Неверный id.")
        try:
            return f"Запись удалена: {self.repository.delete(id)}"
        except ValueError as e:
            raise UserWarning(e)

    @staticmethod
    def _print_title():
        """Печатает шапку."""
        print("id".center(4) + "|" + "сумма".center(7) + "|" + "дата".center(12) + "|" + " описание")
