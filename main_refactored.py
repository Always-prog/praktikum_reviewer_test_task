import datetime as dt
from abc import ABC


class Record:
    """
    Класс служит объектом записей для класса Calculator.
    """
    def __init__(self, amount: float, comment: str = '', date: dt.datetime = None):
        """
        :param amount: Число с плавающей точкой, служит значением записи.
        :param comment: Комментарий к записи.
        :param date: Дата записи
        """
        self.amount = amount
        self.date = dt.datetime.now().date() if date is None else date
        self.comment = comment

    def __str__(self):
        """
        :return: Возвращается <ID-записи>: <amount>, <comment>, <date>
        """
        return f'{id(self)}: amount: {self.amount},comment: {self.comment},date: {self.date}'


class Calculator(ABC):
    """
    Базовый класс калькулятора, позволяющий:
     - Записывать Records
     - Получать Records за последние 7 дней, или за последний день.
     - Получать данные о превышении указанного лимита за последние 7 дней, или за последний день.
    """
    def __init__(self, limit):
        """
        :param limit: Лимит данных записанных в Records.
        """
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for record in self.records:
            today = dt.datetime.now().date()
            if (record.date.day, record.date.year, record.date.month) == (today.day, today.year, today.month):
                today_stats = today_stats + record.amount

        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (today - record.date).days < 7:
                week_stats += record.amount
        return week_stats

    @property
    def today_limit_cross(self):
        return self.limit - self.get_today_stats()

    @property
    def week_limit_cross(self):
        return self.limit - self.get_week_stats()


class CaloriesCalculator(Calculator):
    """
    Данный калькулятор считает, сколько калорий еще можно съесть.
    Для этого при инициализации выставьте лимит, и при каждом потреблении калорий делайте запись Record.
    """
    def get_calories_remained(self):
        """
        Считает остаток калорий на сегодня
        :return:
        """
        if self.today_limit_cross > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {self.today_limit_cross} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """
    Калькулятор считает потраченные деньги за последнюю неделю,
    и имеет возможность выдавать результат в различных курсах валют.
    """
    RUB_RATE = float(1)  # Курс Рубля. Это опорная точка остальных курсов.
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def _get_cash_remained_today(self, currency_type: str):
        """
        :param currency_type: Тип валюты, например USD, EUR, и.т.д.
        :return: Потраченные деньги, с учетом курса валют.
        """
        currency_factory = {
            'usd': lambda cash_remained: cash_remained / self.USD_RATE,
            'eur': lambda cash_remained: cash_remained / self.EURO_RATE,
            'rub': lambda cash_remained: cash_remained / self.RUB_RATE,
        }
        if not currency_type.lower() in currency_factory:
            raise ValueError(f'Указан не обрабатываемый тип валюты {currency_type}, '
                             f'доступные типы: {tuple(currency_factory.keys())}')
        return currency_factory[currency_type.lower()](self.today_limit_cross)

    def get_today_cash_remained(self, currency_type):
        """
        :param currency_type: Тип валюты, например USD, EUR, и.т.д.
        :return: Советы по использованию средств.
        """
        cash_remained = self._get_cash_remained_today(currency_type=currency_type)

        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'

        elif cash_remained < 0:
            return f'Денег нет, держись: твой долг - {-cash_remained:.2f} {currency_type}'

    def get_week_stats(self):
        super().get_week_stats()
