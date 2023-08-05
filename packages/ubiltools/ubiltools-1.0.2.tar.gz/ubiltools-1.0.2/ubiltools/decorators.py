def debug_logger(function):
    import logging

    logging.basicConfig(filename="run.log", level=logging.DEBUG)

    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.NOTSET)

    def inner(*args, **kwargs):
        _logger.info(
            'EXECUTING: {}({}{}{})'.format(function.__name__,
                                           ', '.join(args),
                                           ', ' if len(args) != 0 and len(kwargs) != 0 else '',
                                           ', '.join(['%s=%r' % x for x in kwargs.items()])))
        return function(*args, **kwargs)

    return inner
