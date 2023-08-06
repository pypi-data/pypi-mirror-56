import logging.config
import os

from dotenv import load_dotenv

logging.config.fileConfig('logging.ini')
logger = logging.getLogger()


def load_env():
    if not load_dotenv(override=False):
        logger.info('Could not find any .env file. The module will depend on system env only')


def validate_required_env():
    if os.environ.get('ENVIRONMENT') is None or \
            os.environ.get('ENVIRONMENT').lower() not in ['local', 'dev', 'staging', 'prod']:
        raise ValueError('Incorrect ENVIRONMENT = {}'.format(os.environ.get('ENVIRONMENT')))

    if os.environ.get('REGION') is None:
        raise ValueError('Incorrect REGION = {}'.format(os.environ.get('REGION')))


def override_log_levels():
    if os.environ.get('LOG_LEVEL') is not None and os.environ.get('LOG_LEVEL') in ['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                                                                   'CRITICAL']:
        for handler in logger.handlers:
            try:
                if isinstance(handler, type(logging.FileHandler('../logs/sqlconnection_info.log'))):
                    if 'info.log' in handler.baseFilename:
                        handler.setLevel(os.environ.get('LOG_LEVEL'))
                        logger.info(
                            'Log level={} for filename={}'.format(os.environ.get('LOG_LEVEL'), handler.baseFilename))
                elif isinstance(handler, type(logging.StreamHandler())):
                    handler.setLevel(os.environ.get('LOG_LEVEL'))
                    logger.info('Log level={} for StreamHandler-console'.format(os.environ.get('LOG_LEVEL')))

            except Exception:
                logger.warning('Not able to override LOG_LEVEL for handler={}'.format(str(handler)), exc_info=True)


if __name__ == 'sqlconnection':
    load_env()
    override_log_levels()
    validate_required_env()
    logger.info("Load module = {}, environment={}, region={}\n".format(
        os.environ.get('APP_NAME'), os.environ.get('ENVIRONMENT'), os.environ.get('REGION')))
