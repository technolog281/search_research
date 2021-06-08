from search_research import select
from loguru import logger

if __name__ == '__main__':
    logger.info('Application is running')
    select()
    logger.info('Application is stopped with no errors')

input('Press Enter to exit')
