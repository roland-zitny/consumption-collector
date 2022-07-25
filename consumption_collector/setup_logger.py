import logging


_nameToLevel = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}


def log_level(level) -> int:
    """
        Method convert text representation of log level to int log level.
    """
    if isinstance(level, str):
        _level = level.upper()
        if _level not in _nameToLevel:
            raise AttributeError('Unknown log level "{}"'.format(level))
        return _nameToLevel[_level]
    return level


logger = logging.getLogger('collector')
#logger.setLevel(log_level(get_config('LOGGER_LEVEL')))