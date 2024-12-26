import logging
import pandas as pd
from typing import Union, IO

logger = logging.getLogger(__name__)


def parse_file(file_path: Union[IO, str]) -> pd.DataFrame:
    logger.info(
        f"Начало обработки файла: {file_path if isinstance(file_path, str) else 'файл из потока'}"
    )
    try:
        # Чтение файла в DataFrame
        df = pd.read_excel(file_path, skiprows=2, header=None)
        logger.info("Файл успешно прочитан в DataFrame")

        # Выбор и переименование столбцов
        df = df.iloc[:, [0, 1, 4, 5]]
        df.columns = ["Филиал", "Сотрудник", "Налоговая база", "Исчислено всего"]
        logger.debug(f"Столбцы после обработки: {df.columns.tolist()}")

        # Удаление строк с пустыми значениями в ключевых столбцах
        df.dropna(
            subset=["Филиал", "Сотрудник", "Налоговая база", "Исчислено всего"],
            inplace=True,
        )
        logger.info("Пустые строки удалены из DataFrame")

        return df
    except Exception as e:
        logger.error(f"Ошибка обработки файла: {str(e)}", exc_info=True)
        raise
