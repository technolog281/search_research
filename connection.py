import pymssql
from loguru import logger
import yaml
import psutil


def db_connect():
    with open('./conn_data.yaml') as conn_data:
        logger.info('Load templates for SQL_Connect')
        templates = yaml.safe_load(conn_data)[0]
        db = templates['database']
        if templates is None:
            logger.warning('Templates for SQL_Connect is not load')
        else:
            logger.info('Templates for SQL_Connect is load')
        conn_data.close()
        logger.info('conn_data.yaml is closed')
    try:
        logger.info(f'Trying connect to DB {templates["server"]}:{templates["database"]}')
        conn = pymssql.connect(server=templates['server'],
                               user=templates['user'],
                               password=templates['password'],
                               database=templates['database'],
                               charset=templates['charset'])
        cursor = conn.cursor()
        conn.cursor()
    except pymssql._pymssql.OperationalError:
        logger.error('Connection error, check templates in "conn_data.yaml"')
    else:
        logger.info('Connection established')
        return cursor

#
# def path_finder():
#     try:
#         service = psutil.win_service_get('UnigateIntServ')
#         service_status = service.status()
#         if service_status == 'stopped':
#             logger.info('Service "UnigateIntServ" is stopped now')
#         elif service_status == "running":
#             logger.info('Service "UnigateIntServ" is running')
#             path_to_service = service.binpath()
#             return path_to_service
#     except psutil.NoSuchProcess:
#         logger.error('No such process: "UnigateIntServ"')
