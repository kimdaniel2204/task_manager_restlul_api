import logging
import sys

# Формат логов: Время - Уровень - Сообщение
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler("app.log"), # Логи будут сохраняться в файл
            logging.StreamHandler(sys.stdout) # И дублироваться в терминал
        ]
    )
    return logging.getLogger("task_manager")

logger = setup_logging()