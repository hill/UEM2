import logging
from fastapi.logger import logger
from rich.logging import RichHandler


rich_handler = RichHandler()


def disable_uvicorn_root_logger():
    """Uvicorn adds a default handler to the root logger, so all logs messages are duplicated"""
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.propagate = False


disable_uvicorn_root_logger()

if logger.hasHandlers():
    logger.handlers.clear()

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[rich_handler]
)

log = logging.getLogger("uem")
