import logging


logging.basicConfig(filename=f'test.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug(1 + 1)
