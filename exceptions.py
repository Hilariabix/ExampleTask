from utils import get_config


class TableEmptyException(Exception):
    def __init__(self, table):
        self.table = table

    def __str__(self):
        return "There is no data in {}'s table".format(self.table)


class NoDataException(Exception):
    def __init__(self, table):
        self.table = table

    def __str__(self):
        return "There was no new data for table {}".format(self.table)


class CollectionConnectionError(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return 'There was a problem to communicate with address {}\n' \
               'please check internet connection'.format(self.url)
