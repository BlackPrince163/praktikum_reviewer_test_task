import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # "not" лучше перенести на верхнюю строчку. Это повысит читаемость кода.
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    # Лучше сделать class метод, потому что используется только внутренние аргументы. Посмотри пожалуйста видео:
    # https://www.youtube.com/watch?v=rZY9CJn1y2E
    def get_today_stats(self):
        today_stats = 0
        # Не стоит называть переменную в python c большой буквой. Это не соответствует стандарту pep-8. Вот подробная
        # статья про это: https://clck.ru/324oix
        for Record in self.records:
            # вынести "dt.datetime.now().date()" за цикл. Вдруг во время выполнение программы поменяется дата. Надо
            # сделать как в ~40 строчке.
            if Record.date == dt.datetime.now().date():
                # Лучше использовать today_stats += Record.amount. Так меньше кода используется и не ухудшается
                # читабельность кода
                today_stats = today_stats + Record.amount
        return today_stats

    # и это тоже лучше сделать class метод
    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Сlass method как в 23 строчке
    # Комментарий спустить вниз и написать так docstring. Статья про это:
    # https://dvmn.org/encyclopedia/qna/13/chto-takoe-docstring-s-chem-ego-edjat/
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Здесь лучше создать новый метод, который будет реализовать парсинг курсов валют, потому что курс доллара и курс
    # евро могут меняться. На данном курсе это неважно поэтому в новом методе можно просто объявить и вернуть константу
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Не стоит называть аргументы с большой буквой, как и переменные. Об этом мы с тобой читали в 28 строчке.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
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
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()
