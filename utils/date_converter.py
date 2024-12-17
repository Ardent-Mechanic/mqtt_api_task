from datetime import datetime


def convert_to_date(date_str: str, format: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Преобразует строку в объект datetime.datetime, включая расчет времени (часы, минуты, секунды).

    :param date_str: Строка с датой и временем, например, '2024-12-17 15:30:45'.
    :param format: Формат даты и времени (по умолчанию '%Y-%m-%d %H:%M:%S').
    :return: Объект datetime.datetime.
    """
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        raise ValueError(f"Неверный формат даты и времени: '{date_str}'. Ожидался формат '{format}'.")
