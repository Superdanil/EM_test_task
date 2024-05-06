from dataclasses import dataclass
from datetime import datetime, date
from typing import Literal
import config


@dataclass
class RecordModel:
    """Датакласс записей, хранящихся в электронном кошельке."""
    category: Literal["доход", "расход"]
    value: int
    date: str
    description: str
    id: int | None = None

    def __post_init__(self):
        self._description = self.description
        self._date = self.date
        self._value = self.value
        self._id = self.id

    @property
    def _description(self) -> str:
        return self._description

    @_description.setter
    def _description(self, data: str) -> None:
        """Функция валидации поля описания."""
        if config.MIN_DESCRIPTION_LENGTH <= len(data) <= config.MAX_DESCRIPTION_LENGTH:
            self.description = data
        else:
            raise ValueError(f"Длина описания должна составлять от {config.MIN_DESCRIPTION_LENGTH} до "
                             f"{config.MAX_DESCRIPTION_LENGTH} символов.")

    @property
    def _date(self) -> str:
        return self._date

    @_date.setter
    def _date(self, data: str) -> None:
        """Функция валидации поля даты."""
        try:
            datetime.strptime(data, config.DATE_PATTERN)
            self.date = data
        except ValueError:
            raise ValueError(f"Неверный формат даты.")

    @property
    def _value(self) -> int:
        return self._value

    @_value.setter
    def _value(self, data: str) -> None:
        """Функция валидации поля величины дохода/расхода."""
        try:
            if data.isdigit():
                self.value = int(data)
            else:
                raise ValueError(f"Величина дохода/расхода должна быть числом.")
        except AttributeError:
            pass

    @property
    def _id(self) -> int | None:
        return self._id

    @_id.setter
    def _id(self, data: str | None) -> None:
        """Функция валидации поля id."""
        if data is not None:
            try:
                if data.isdigit():
                    self.id = int(data)
                else:
                    raise ValueError(f"id должен быть целым числом.")
            except AttributeError:
                pass

    def __str__(self):
        pretty_id = str(self.id).center(4)
        pretty_category = "+" if self.category == "доход" else "-"
        pretty_value = str(self.value).ljust(6)
        pretty_date = self.date.center(12)
        return f"{pretty_id}|{pretty_category}{pretty_value}|{pretty_date}| {self.description}"
