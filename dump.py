from random import randint, choice, shuffle

from record_model import RecordModel
from repository import WalletRepository

incomes_categories = ["зарплата", "инвестиции", "авито", "нашёл"]
expenses_categories = ["продукты", "авто", "такси", "кафе", "одежда", "электроника", "кот"]

records = []

for i in range(10):
    rec = RecordModel(
        category="доход",
        value=randint(1000, 20000),
        date=f"{randint(1, 28)}.{randint(1, 12)}.2024",
        description=choice(incomes_categories)
    )
    records.append(rec)

for i in range(50):
    rec = RecordModel(
        category="расход",
        value=randint(100, 3000),
        date=f"{randint(1, 28)}.{randint(1, 12)}.2024",
        description=choice(expenses_categories)
    )
    records.append(rec)

shuffle(records)

for rec in records:
    WalletRepository().add(rec)
