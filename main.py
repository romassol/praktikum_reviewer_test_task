import datetime as dt
import json  # Нужно удалять неиспользуемые импорты, так как это загромождает код и усложняет читаемость

# Не соблюдаются общие требования к коду. По pep8 -
# перед классами должно быть 2 пустые строки,
# вокруг операторов должны быть пробелы,
# перед методами класса должен быть отступ в 1 строку.
# Длина строки не должна превышать 79 символов.
# Это все сильно уссложняет читаемость кода.
# Для автоматического обнаружения таких ошибок удобно использовать линтеры -
# pylint, например

class Record:
    # Шаблон для даты стоит вынести в константу, чтобы код было проще
    # изменять в будущем. Константа всегда сверху файла, и не нужно
    # будет искать по всему коду нужное место. То есть перед __init__
    # добавится DATE_TEMPLATE = '%d.%m.%Y'

    # В качестве значения по умолчанию параметра date не должна быть
    # пустая строка, должна быть текущая дата, то есть
    # date=dt.datetime.now().date()
    def __init__(self, amount, comment, date=''):
        self.amount=amount
        # Тогда тут с изменениями выше изменится до
        # self.date = dt.datetime.strptime(date, self.DATE_RECORD_TEMPLATE).date() if isinstance(date, str) else date
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment=comment

# Так как это базовый класс, и не подразумевается создавать его экземпляры,
# стоит сделать его базовым классом. Для этого в импорты нужно добавить
# import abc (не забудь про сортировку импортов), а строку ниже изменить на
# class Calculator(abc.ABC):


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records=[]
    def add_record(self, record):
        self.records.append(record)
    def get_today_stats(self):
        today_stats=0
        # переменные стоит называть с маленькой буквы, тем более в этом
        # случае название переменной - Record совпадает с названием класса выше,
        # поэтому могут возникнуть проблемы, если захочещь внутри цикла
        # обратиться к классу Records.
        # Но ввесь код этого метода можно было сократить с использованием
        # генераторного выражения до
        # return sum(
        #     record.amount for record in self.records
        #     if record.date == dt.datetime.now().date()
        # )
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats+Record.amount
        return today_stats
    def get_week_stats(self):
        week_stats=0
        today = dt.datetime.now().date()
        for record in self.records:
            # это неравенство можно сократить до
            # 0 <= (today - record.date).days < 7. Но так же, как и в
            # get_today_stats можно использовать генераторное выражение и
            # еще сократить весь код этого метода.
            if (today -  record.date).days <7 and (today -  record.date).days >=0:
                week_stats +=record.amount
        return week_stats
class CaloriesCalculator(Calculator):
    # Здесь комментарий излишен, так как название метода отражает всю суть
    def get_calories_remained(self): # Получает остаток калорий на сегодня
        # Стоит переименовать переменную x на remaining_calories, например,
        # чтобы название переменной отражало суть значения
        x=self.limit-self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        # else в данном случае излишен, так как если x <= 0,
        # то мы все равно вернем 'Хватит есть!'
        else:
            return 'Хватит есть!'
class CashCalculator(Calculator):
    # Не нужно преобразовывать курсы валют во float, во время вычислений
    # они сами преобразуются, если это нужно будет.
    # Комментарии излишни, названия констант и так отражают всю их суть.
    USD_RATE=float(60) #Курс доллар США.
    EURO_RATE=float(70) #Курс Евро.
    # По условию задачи метод должен принимать только валюту, к константам
    # курса валют внутри метода можно обратитьсся через self -
    # self.USD_RATE, self.EURO_RATE
    # Еще стоит создать для валют enum - набор имен, привязанных к уникальным
    # постоянным значениям. У нас как раз этот метод должен принимать
    # определенные константы - одно из строк "rub", "usd" или "eur".
    # Подробнее про enum - https://docs.python.org/3/library/enum.html
    def get_today_cash_remained(self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Для определения типа валюты стоит вынести константу в начало класса,
        # например, CURRENCY_TO_CURRENCY_TYPE. Это будет словарь, где в
        # качестве ключей будут ключи enum`а, а в качестве значений типы
        # констант которые соответствуют конкретной валюте. Выглядеть это будет
        # примерно так
        # CURRENCY_TO_CURRENCY_TYPE = {
        #         Currency.USD: 'USD',
        #         Currency.EURO: 'Euro',
        #         Currency.RUB: 'руб'
        #     }
        # А если валюта из аргументов не соответствует ни одному значению
        # из словаря, то стоит напечать, что калькулятор не поддерживает данный
        # тип валюты.
        # Благодаря этому легче будет изменять код, добавлять новые валюты +
        # добавилась обработка в случае неподдерживаемой валюты.
        currency_type=currency
        cash_remained = self.limit - self.get_today_stats()
        if currency=='usd':
            cash_remained /= USD_RATE
            currency_type ='USD'
        elif currency_type=='eur':
            cash_remained /= EURO_RATE
            currency_type ='Euro'
        elif currency_type=='rub':
            # это лишнее, если у нас в качестве валюты рубли, то нам можно
            # никак не преобразовывать деньги
            cash_remained == 1.00
            currency_type ='руб'
        if cash_remained > 0:
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Можно без этого elif - просто return, так как до этого уже покрыли
        # случаи >= 0, значит остались только сслучаи < 0
        elif cash_remained < 0:
            # Стоит исспользовать f-строки, так как до этого в коде они всегда
            # использовались.
            # Еще по условию задачи долг нужно печатать положительным числом
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)
        # Чтобы повысить читаемость кода, можно вынести в отдельные приватные
        # методы конвертацию денег и получение итогового сообщения. Приватные
        # методы - методы, которые начинаются с _, в них содержится логика,
        # которая не понадобится пользователям класса, поэтому в среде
        # разработки после . они не показываются в списке всех методов класса.
        # В итоге тело этого метода преобразится примерно в
        # if currency not in self.CURRENCY_TO_CURRENCY_TYPE:
        #     return 'Нет данной валюты'
        # cash_remained = self.limit - self.get_today_stats()
        # cash_remained = self._convert_cash_by_currency(cash_remained, currency)
        # currency_type = self.CURRENCY_TO_CURRENCY_TYPE[Currency(currency)]
        # return self._get_message_by_cash_remained(cash_remained, currency_type)

    # Этот метод можно удалить, так как внутри нет никакой дополнительной
    # логики, кроме логики родительского класса
    def get_week_stats(self):
        super().get_week_stats()
