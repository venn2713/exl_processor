import logging
import pandas as pd
from typing import Union, IO

logger = logging.getLogger(__name__)


def parse_file(file_path: Union[IO, str]) -> pd.DataFrame:
    logger.info(
        f"Начало обработки файла: {file_path if isinstance(file_path, str) else 'файл из потока'}"
    )
    try:
        # Считываем весь файл, включая заголовки
        df = pd.read_excel(file_path, skiprows=None, header=None, engine="openpyxl")
        logger.info("Файл успешно прочитан в DataFrame")

        # Проверяем, содержит ли файл данные, помимо заголовков
        if df.shape[0] <= 2:  # Если в файле только заголовки или меньше 3 строк
            raise ValueError("Файл пуст. Загрузка данных невозможна.")

        if df.shape[1] < 6:
            raise ValueError("Файл должен содержать минимум 6 столбцов.")

        # Проверяем структуру заголовков
        header_row_1 = df.iloc[0].fillna("").tolist()
        header_row_2 = df.iloc[1].fillna("").tolist()
        expected_headers_1 = [
            "Филиал",
            "Сотрудник",
            "Доход",
            "Вычеты",
            "Налоговая база",
            "Налог",
        ]
        expected_headers_2 = [
            "",
            "",
            "Начислено",
            "Вычеты всего",
            "",
            "Исчислено всего",
            "Удержано всего",
        ]

        if (
            header_row_1[:6] != expected_headers_1
            or header_row_2[:7] != expected_headers_2
        ):
            raise ValueError(
                "Файл имеет некорректную структуру. Проверьте исходные данные."
            )

        # Считываем только данные, начиная с третьей строки
        df = pd.read_excel(file_path, skiprows=2, header=None, engine="openpyxl")

        df = df.iloc[:, [0, 1, 4, 5]]
        df.columns = ["Филиал", "Сотрудник", "Налоговая база", "Исчислено всего"]

        # Удаляем строки с пустыми значениями в обязательных столбцах
        required_columns = ["Филиал", "Сотрудник", "Налоговая база", "Исчислено всего"]
        df.dropna(subset=required_columns, inplace=True)

        if df.empty:
            raise ValueError(
                "Файл не содержит валидных данных после удаления пустых строк."
            )

        logger.info("Пустые строки удалены из DataFrame")
        return df

    except ValueError as ve:
        logger.error(f"Ошибка валидации файла: {str(ve)}", exc_info=False)
        raise
    except Exception as e:
        logger.error(f"Ошибка обработки файла: {str(e)}", exc_info=False)
        raise
