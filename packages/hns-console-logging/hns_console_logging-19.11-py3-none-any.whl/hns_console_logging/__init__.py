import logging


def get_logger(module,
               log_format='%(asctime)s %(name)s %(funcName)s[PID:%(process)d TID:%(thread)d] %(levelname)s %(message)s',
               log_level=logging.INFO):
    """ Creates a logger """

    logger = logging.getLogger(module)
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(logging.Formatter(log_format))
    logger.addHandler(ch)
    return logger
