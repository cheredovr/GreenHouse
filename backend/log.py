import logging

def setup_logging(
    log_level=logging.INFO,
    log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    date_format='%Y-%m-%d %H:%M:%S'
):
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler()]
    )
    logging.info("Логгирование в консоль успешно настроено")