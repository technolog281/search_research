import gzip

from loguru import logger
import psutil
import os


def num_parse(list_of_strings):    # Парсит коды исследований из файла логов по указанным ошибкам, выдаёт список кодов
    list_of_numbers_unilog = []
    for i in list_of_strings:
        if 'Нет сопоставления с кодом' in i:
            research_num = i.split('м ')[1]
            if len(research_num) > 3:
                logger.info(f'Find research with Code = "{research_num}"')
                list_of_numbers_unilog.append(research_num)
    return list_of_numbers_unilog


def path_finder():  # Проверяет наличие и статус unigateIntServ на ПК, выдаёт путь к корню unigateIntServ
    try:
        service = psutil.win_service_get('UnigateIntServ')
        service_status = service.status()
        if service_status == 'stopped':
            logger.info('Service "UnigateIntServ" is stopped now')
        elif service_status == 'running':
            logger.info('Service "UnigateIntServ" is running')
            path_to_service = service.binpath()
            return path_to_service
    except psutil.NoSuchProcess:
        logger.error('No such process: "UnigateIntServ"')


def log_executer():  # Извлекает пути к файлам логов в список, выдаёт список путей
    list_of_numbers = []
    unigate_path = path_finder().rsplit('/', 1)[0] + '/log'
    unigate_path = unigate_path.replace("C://", 'C:/')
    log_folders_list = os.listdir(path=unigate_path)
    if 'unigateIntServ.log' in log_folders_list:
        unigateIntServ_path = unigate_path + '/unigateIntServ.log'
        try:
            with open(unigateIntServ_path, encoding='cp1251') as fh:  # Слабое место, ожидается баг encoding
                list_of_strings = fh.read().split("\n")
                list_of_numbers = list_of_numbers + num_parse(list_of_strings)
            fh.close()
        except FileNotFoundError:
            logger.error(f'Log-file not found in {unigateIntServ_path}')
        log_folders_list.remove('unigateIntServ.log')
    for every in log_folders_list:
        logger.info(f'Found logs for {every}')
        log_gz_list = os.listdir(unigate_path + f'/{every}')
        for everyone in log_gz_list:
            file_path = unigate_path + '/' + every + '/' + everyone
            with gzip.open(file_path, 'rt', encoding='Windows-1251') as log:
                logger.info(f'Reading {file_path}, please wait...')
                fin = log.read()
                list_of_strings = fin.split("\n")
                logger.info(f'Parsing {file_path}, please wait...')
                list_of_numbers = list_of_numbers + num_parse(list_of_strings)
    return list(set(list_of_numbers))


print(log_executer())
