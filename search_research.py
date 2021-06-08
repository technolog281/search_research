from itertools import groupby
from loguru import logger
import pandas as pd
import pymssql
import yaml

logger.add('logs.log')

dict_to_df = {}
list_of_numbers = []

try:
    with open('./conn_data.yaml') as conn_data:
        logger.info('Opening UnigateInsServ.log templates')
        link_templates = yaml.safe_load(conn_data)[1]
        print(link_templates)
        if link_templates is None:
            logger.warning('UnigateInsServ.log templates not open')
        else:
            logger.info('Open UnigateInsServ.log templates')
except FileNotFoundError:
    logger.error('YAML-Configuration file not found in "./conn_data.yaml"')

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


def num_parse():
    with open(link_templates['log_link'], encoding=link_templates['encoding']) as fh:
        abra = fh.read()
        list_of_strings = abra.split("\n")
    for i in list_of_strings:
        if 'Нет сопоставления с кодом' in i:
            research_num = i.split('м ')[1]
            if len(research_num) > 3:
                logger.info(f'Find research with Code = "{research_num}"')
                list_of_numbers.append(research_num)
    fh.close()
    return list_of_numbers


def db_connect():
    conn = pymssql.connect(server=templates['server'],
                           user=templates['user'],
                           password=templates['password'],
                           database=templates['database'],
                           charset=templates['charset'])
    res_cursor = conn.cursor()
    return res_cursor


try:
    db_connect()
except pymssql._pymssql.OperationalError:
    logger.exception('Connection error, check templates in "conn_data.yaml"')
else:
    logger.info(f'Connection to {db} was successful')


def select():
    df = pd.DataFrame(columns=['UnigateCode', 'ResearchName'])
    cursor = db_connect()
    for num in num_parse():
        cursor.execute(f"select ParamName from lbr_researchtypeparam where codelis = '{num}'")
        uguid_list = str(cursor.fetchall())
        uguid_split = uguid_list.split("'")
        research_name_list = []
        for uguid in uguid_split:
            if len(uguid) > 5:
                research_name_list.append(uguid)
                research_name_string = str([el for el, _ in groupby(research_name_list)])
                research_name = research_name_string.split("'")
                x = ''
                for every in research_name:
                    if len(every) > 5:
                        x = x + every + ', '
        df = df.append({'UnigateCode': num, 'ResearchName': x.rsplit(',', 1)[0]}, ignore_index=True, sort=False)
        logger.info(f'For research {num}, a match was found - {x}')
    df.to_excel('./result.xlsx', index=False)
    logger.info('Research list was write to "result.xlsx"')


