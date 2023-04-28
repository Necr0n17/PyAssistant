from pycodestyle import Checker
from contextlib import redirect_stdout
import os
import io


class ErrorReport:
    def __init__(self, checker_result: str):
        """Класс для хранения информации об определённой ошибке в коде
        пользователя и извлечения её в удобном для чтения пользователю
        формате"""
        self.str_number = int(checker_result.split(':')[1])
        self.letter_number = int(checker_result.split(':')[2])
        self.error_code = checker_result.split()[1]
        self.description = ' '.join(checker_result.split()[2:])

    def report(self):
        """Возвращает информацию об ошибке в удобном для чтения формате"""
        return f'{self.str_number} строка, {self.letter_number} символ: ' \
               f'{self.error_code} - {self.description}'


def process():
    """Проверяет код, записанный в файл code.py, на наличие ошибок"""

    # Создаёт объект класса Checker, который будет проверять код пользователя.
    # В аргумент ignore записываем номер ошибки W391. Она совсем
    # незначительна и программа будет её игнорировать.
    fchecker = Checker('code.py', show_source=True, ignore='W391')

    # Читает результат проверки fchecker. Checker выводит результат в
    # консоль, а не просто возвращает при помощи return, поэтому необходимо
    # использовать redirect_stdout.
    f = io.StringIO()
    with redirect_stdout(f):
        # проверка кода
        fchecker.check_all()

    # Преобразует результат в объекты класса ErrorReport, хранящих
    # информацию о полученных ошибках. Берётся каждая третья строка вывода,
    # так как другие две визуально показывают содержимое строки и указывают
    # на символ с ошибкой - боту эта визуализация не нужна, а для
    # пользователя будет слишком громоздко.
    return [ErrorReport(i) for i in f.getvalue().splitlines()[::3]]


def corrections():
    """Исправляет ошибки оформления кода, записанного в файл code.py,
    и делает его в общем чуть более читаемым для других программистов"""

    # Пишем в консоль команду для исправления кода пользователя.
    os.system('black code.py')
