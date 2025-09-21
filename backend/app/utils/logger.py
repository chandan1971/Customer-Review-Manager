import logging

def get_logger(name: str):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    return logger
