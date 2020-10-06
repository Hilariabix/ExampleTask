import logging

import yaml


def get_config():
    with open(r'config.yml') as file:
        return yaml.load(file)


def get_logger():
    lgr = logging.getLogger(__name__)
    lgr.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

    file_handler = logging.FileHandler('logfile.log')
    file_handler.setFormatter(formatter)
    lgr.addHandler(file_handler)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    lgr.addHandler(ch)
    return lgr
