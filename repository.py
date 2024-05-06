from datetime import datetime

import config
from record_model import RecordModel


class WalletRepository:
    """Класс операций чтения/записи/обновления/удаления записей в кошельке."""

    def __init__(self):
        self.database = "wallet.txt"
        self.last_id = 0

    def add(self, record: RecordModel) -> RecordModel:
        """Добавляет запись в кошелёк."""
        record.id = self._get_last_id() + 1
        with open(self.database, "a") as file:
            file.writelines([str(record.__dict__), "\n"])
        return record

    def _get_last_id(self) -> int:
        """Возвращает номер последней записи в кошельке."""
        with open(self.database, "r") as file:
            try:
                last_rec = eval(file.readlines()[-1])
            except IndexError:
                return 0

        return last_rec["id"]

    def get_balance(self) -> dict:
        """Возвращает текущий баланс кошелька, сумму всех доходов и расходов."""
        incomes = 0
        expenses = 0
        with open(self.database, "r") as file:
            try:
                for line in file:
                    record = RecordModel(**eval(line))
                    if record.category == "доход":
                        incomes += record.value
                    elif record.category == "расход":
                        expenses += record.value
                balance = incomes - expenses
                wallet_state = {"баланс": balance, "доходы": incomes, "расходы": expenses}
            except IndexError:
                wallet_state = {"баланс": 0, "доходы": 0, "расходы": 0}
            finally:
                return wallet_state

    def get_records(self, **kwargs) -> list[RecordModel]:
        """Возвращает список записей из кошелька согласно фильтру в kwargs."""
        records = []
        with open(self.database, "r") as file:
            try:
                for line in file:
                    record = RecordModel(**eval(line))
                    if kwargs:
                        for key, value in kwargs.items():
                            if key != "date":
                                if value == record.__dict__[key]:
                                    records.append(record)
                            else:
                                if value in record.__dict__["date"]:
                                    records.append(record)
                    else:
                        records.append(record)
                return sorted(records, key=lambda x: datetime.strptime(x.date, config.DATE_PATTERN))
            except IndexError:
                return []

    def update(self, record: RecordModel) -> RecordModel:
        """Полностью обновляет одну запись в кошельке, кроме её id."""
        with open(self.database, "r") as file:
            lines = file.readlines()
            records_found = 0
            for i in range(len(lines)):
                rec = RecordModel(**eval(lines[i]))
                if rec.id == record.id:
                    lines[i] = str(record.__dict__) + "\n"
                    records_found += 1
                    break
            if records_found == 0:
                raise ValueError("Неверный id.")
        with open(self.database, "w") as file:
            file.writelines(lines)

        return record

    def delete(self, id: int) -> RecordModel:
        with open(self.database, "r") as file:
            lines = file.readlines()
            records_found = 0
            for i in range(len(lines)):
                rec = RecordModel(**eval(lines[i]))
                if rec.id == id:
                    lines.remove(lines[i])
                    records_found += 1
                    break
            if records_found == 0:
                raise ValueError("Неверный id.")
        with open(self.database, "w") as file:
            file.writelines(lines)

        return rec
