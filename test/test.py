



def log():
    logging.debug('Start')
    logging.info('Exec')
    logging.info('Finished')


if __name__ == '__main__':
    setup_logging(yaml_path)
    logger = logging.getLogger('main.core')
    logger.info('First Try')
    logger.info('Second Try')
    log()


