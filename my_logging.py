import logging
import os


class Log:
    def __init__(self):
        folder_log = 'log\\'
        name_log = 'log_parse.log'
        date_format = '%d_%m_%Y %H_%M_%S'

        self.filename = folder_log+name_log
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                       filename=self.filename,
                                       datefmt=date_format,
                                       level=logging.INFO
                                       )

    def write_log(self, message):
        if not os.path.isfile(self.filename):
            logging.info('Create Log File')

        if message[0] == 'error':
            logging.error(message[1])
        elif message[0] == 'info':
            logging.info(message[1])
        elif message[0] == 'warning':
            logging.warning(message[1])
        else:
            logging.debug(message[1])


if __name__ == '__main__':
    mass = ['info', 1]
    print(mass[0], mass[1])
    Log().write_log(mass)