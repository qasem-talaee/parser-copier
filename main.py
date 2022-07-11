import os

from lib import parser, copier

def check_dir():
    if not os.path.isdir('config-copy'):
        os.mkdir('config-copy')
    if not os.path.isdir('config-log'):
        os.mkdir('config-log')

def main():
    my_object_parser = parser.Parser()
    my_object_copy = copier.Copier()
    
    my_object_parser.start()
    my_object_copy.start()
    
if __name__ == '__main__':
    print('\t\tParser and Copier is Starting...\n')
    check_dir()
    main()