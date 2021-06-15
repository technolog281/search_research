import pandas as pd
from loguru import logger
from connection import db_connect
from log_executer import log_executer

logger.add('logs.log')
dict_to_df = {}

cursor = db_connect()


def select():
    df = pd.DataFrame(columns=['UnigateCode', 'ResearchName', 'Research_Code', 'Biom', 'ParamName'])
    for num in log_executer():
        # noinspection SqlResolve
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
                # noinspection SqlResolve
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
