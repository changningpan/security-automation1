import configparser


def ReadConfigfile():
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    filepath = cf.get('Filepath', 'filename')
    return filepath