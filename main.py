from search_research import select
from loguru import logger

if __name__ == '__main__':
    logger.info('Application is running')
    select()
    logger.info('Application is stopped')

input('Press Enter to exit')
