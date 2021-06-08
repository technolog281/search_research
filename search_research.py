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
    logger.error('Connection error, check templates in "conn_data.yaml"')
else:
    logger.info(f'Connection to {db} was successful')

cursor = db_connect()


def select():
    df = pd.DataFrame(columns=['UnigateCode', 'ResearchName', 'Research_Code', 'Biom', 'ParamName'])
    for num in num_parse():
        cursor.execute("SELECT lbr_ResearchType.ResearchName, "
                       "lbr_ResearchType.Code, "
                       "lbr_ResearchType.rf_BioMID, "
                       "lbr_ResearchTypeParam.ParamName "
                       "FROM lbr_ResearchType JOIN lbr_ResearchTypeParam "
                       "ON lbr_ResearchType.UGUID = lbr_ResearchTypeParam.rf_ResearchTypeUGUID "
                       f"WHERE CodeLis = '{num}'")
        biom_list = cursor.fetchall()
        if biom_list is not None:
            logger.info(f'For research {num}, a match was found')
        if len(biom_list) >= 1:
            for one in biom_list:
                cursor.execute(f"SELECT Name FROM lbr_BioM WHERE BioMID = '{one[2]}'")
                biom_name = cursor.fetchone()
                df = df.append({'UnigateCode': num,
                                'ResearchName': one[0],
                                'Research_Code': one[1],
                                'Biom': biom_name[0],
                                'ParamName': one[3]},
                               ignore_index=True)
    df.to_excel('result.xlsx')
    logger.info('Research list was write to "result.xlsx"')
