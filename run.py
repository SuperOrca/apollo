from bot import Apollo
from os import environ

if __name__ == '__main__':
    environ['JISHAKU_UNDERSCORE'] = 'True'
    environ['JISHAKU_HIDE'] = 'True'
    Apollo().run()
