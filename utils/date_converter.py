from datetime import datetime


# Функция преобразования строки в дату
def convert_to_date(date_str: str, format: str = "%Y-%m-%d") -> datetime.date:
    """
    Преобразует строку в объект datetime.date.

    :param date_str: Строка с датой, например, '2024-12-17'.
    :param format: Формат даты (по умолчанию '%Y-%m-%d').
    :return: Объект datetime.date.
    """
    try:
        return datetime.strptime(date_str, format).date()
    except ValueError:
        raise ValueError(f"Неверный формат даты: '{date_str}'. Ожидался формат '{format}'.")
