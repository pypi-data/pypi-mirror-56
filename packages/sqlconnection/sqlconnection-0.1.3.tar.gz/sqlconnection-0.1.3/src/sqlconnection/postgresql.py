import sqlconnection
import os
import logging
import psycopg2

logger = logging.getLogger()


class Postgresql:
    def __init__(self):
        logger.debug('Initiating Postgresql Connection Class')
        self.connection_parameter = None
        self.connection = None

    def set_connection_parameter(self):
        self.connection_parameter = {
            "user": os.environ.get('SQL_USER'),
            "password": os.environ.get('SQL_PASSWORD'),
            "host": os.environ.get('SQL_HOST'),
            "port": os.environ.get('SQL_PORT'),
            "database": os.environ.get('SQL_DATABASE')
        }

        return self.connection_parameter

    def create_connection(self):
        if self.connection_parameter is None:
            self.set_connection_parameter()

        try:
            logger.debug('Creating postgres connection')
            conn = psycopg2.connect(user=self.connection_parameter['user'],
                                    password=self.connection_parameter['password'],
                                    host=self.connection_parameter['host'],
                                    port=self.connection_parameter['port'],
                                    database=self.connection_parameter['database'])

            self.connection = conn
            logger.info('Error in making postgres connection with host={}, port={}, user={}, database={}'.format(
                self.connection_parameter['host'], self.connection_parameter['port'], self.connection_parameter['user'],
                self.connection_parameter['database']))
        except Exception as ce:
            logger.error('Error in making postgres connection with host={}, port={}, user={}, database={}'.format(
                self.connection_parameter['host'], self.connection_parameter['port'], self.connection_parameter['user'],
                self.connection_parameter['database']), exc_info=True)
            raise Exception("Connection Error with Postgresql")

    def get_connection(self):
        if self.connection is None:
            self.create_connection()
        return self.connection

    def get_cursor(self):
        return self.get_connection().cursor()

    def close_connection(self):
        if self.connection is not None:
            try:
                self.connection.commit()
                self.connection.close()
            except Exception as e:
                logger.warning('Unable to close postgres connection. Connection might be already closed', exc_info=True)
            self.connection = None
