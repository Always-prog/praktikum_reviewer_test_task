"""Читай замечания сверху вниз, посматривая как то или иное реализованно в отревьюином коде main_refactored.py"""
"""
Архитектура калькулятора хорошая, но требуется доработка в местах:
1. Лимит, установленный в класса Calculator, распространяется как на неделю, так и на день. 
   Лучше сделать лимит на день и использовать при расчетах на дне, и умножать его на 7 при расчетах с неделей.
   
   
Сама реализация не правильная в местах:
1. Неправильный типов аргументов.
2. Нагруженности некоторых функций 
3. Повторения одного и того же расчета, несмотря на то что у нас есть базовые классы для них.
4. Множественные проверки if...elif, вместо ссылки через dict 

Все этим проблемы решены в main_refactored.py, а в этом файле расписано что и как изменено.

Совет изучить:
 - ABC базовые классы, их можно использовать в классе Calculator.
 - property функций, их используют для расчетов в виде переменных.
 - Описание типов данных и аргументов. Библиотеку typing. Код с помощью этого читабельнее, и яснее.
 - Больше про возможности применения словарей (не только как хранение данных, а еще как ссылки). 
   Пример использования словаря как хранителя ссылок смотри в реализации 67 строку в main_refactored, 
   _get_cash_remained_today()
"""

import datetime as dt


class Record:
    # TODO: Сделай описание класса
    def __init__(self, amount, comment, date=''):
        # TODO: Сделай значение по умолчанию date = None
        # Зачем: Это нужно чтобы проверка на None была правильной, через is None
        # TODO: Сделай значение по умолчанию comment = ''
        # Зачем: Коммент пользователя на каждую запись не обязателен,
        #        соответственно у него должна быть возможность его пропустить.
        self.amount = amount

        # TODO: Сделай прием date в типе datetime.date, вместо парсинга ее из строки
        # Зачем: Чтобы сохранять целостность программы, и работать с одним форматом даты, и без парсинга из строки.
        # TODO: Сделай проверки и присвоения к date в одну строчку.
        # Зачем: Так читабельнее
        self.date = (
            dt.datetime.now().date() if
            not date else dt.datetime.strptime(date, '%d.%m.%Y').date())

        self.comment = comment

    # TODO: Добавь функцию __str__() (https://www.educative.io/edpresso/what-is-the-str-method-in-python)
    # Зачем: Чтобы при `print(record)` выводилась нужная информация для пользователя о записи.


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):  # TODO: Добавь тип record: Record, чтобы аргумент был яснее.
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0

        # TODO: Переименуй переменную Record в record.
        # Зачем: Это такое правило среди программистов python,
        # с больших букв называют классы, а переменные - с маленьких.
        for Record in self.records:
            # TODO: Сделай проверку отдельно на год, на месяц и на день.
            # Зачем: это сделает невозможным сбить программу если в дате будет что-то лишнее.
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Единственная проверка которая тебе нужна, это первая `today - record.date).days <= 7`
            if (
                    (today - record.date).days < 7 and # TODO: Добавь <=, т.к. последний день недели тоже включаеться
                    (today - record.date).days >= 0  # TODO: Удали, это лишняя проверка.

            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # TODO: Сделай описание класса.
    # Как делай описание классов правильно, смотри под классами в main_refactored.py
    # Важно указать общее назначение класса и какие аргументы принимает.

    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # TODO: Вместо того чтобы оставлять коментарии после объявления функции,
        #       делай лучше описание под ней, используя специальную структуру описания.
        #       Как описывать функции так, чтобы было понятно любому, смотри в main_refactored под этой же функцией

        x = self.limit - self.get_today_stats()  # TODO: Вынести это в property функцию класса Calculator
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'  # TODO: Вынести текст в одну строчку
        else:
            return ('Хватит есть!')  # TODO: Убери скобки, они лишние тут.


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):  # TODO: Удали передачу курсов отсюда
        currency_type = currency  # TODO: Назови переменную currency_type сразу

        # TODO: Создай property функцию в самом классе Calculator, которая будет считать limit - get_today_stats()
        cash_remained = self.limit - self.get_today_stats()


        # TODO: Вынеси проверки типа денег вне get_today_cash_remained!
        # Зачем:
        # Это нужно чтобы упростить проверки, и сделать возможность возвращать ошибки, сделай следующее:
        # 1. В вынесенной функции сделай словарь,
        #    куда помести все значения currency и функции lambda которые должны считать и возвращать результат.
        # 2. Сделай получение функции lambda по currency, используя функцию .get(),
        #     В случае если get() вернет None, возвращяй ошибку raise ValueError (это будет значить что currency не найден)
        #     Если оно не None - значит все найдено, и функция расчета есть, просто запусти ее и верни результат.

        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00  # TODO: Удали, и вместо этого сделай cash_remained /= EURO_RATE, где EURO_RATE = 1.
            # Строчка выше даже не перезапись cash_remained, а просто условие. Удали.

            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)  # TODO: Используй F строки, как и в коде выше.

    def get_week_stats(self):
        super().get_week_stats()
