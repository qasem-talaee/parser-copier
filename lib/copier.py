import threading
import yaml
import os
import time
import shutil
import datetime

class Copier(threading.Thread):
    
    def __read_yaml(self, infile):
        self.__config = {}
        with open('config-copy/' + infile, 'r') as f:
            docs = yaml.load_all(f, Loader=yaml.FullLoader)
            for doc in docs:
                self.__config = doc
        self.__config['File-Name'] = infile.replace(infile.split('.')[-1], '')
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.__config = {}
    
    def __procc(self, i):
        item = self.__config['Order'][i]
        try:
            list_from = os.listdir(item['From'])
            list_to = os.listdir(item['To'])
        except:
            print('COPIER ERR : Path Does not Exist.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
        else:
            sorted_to = {}
            sorted_from = {}
            for type in item['Type']:
                sorted_to[type] = []
                sorted_from[type] = []
            for type in item['Type']:
                for file in list_to:
                    if type in file:
                        sorted_to[type].append(item['To'] + '\\' + file)
                for file in list_from:
                    if type in file:
                        sorted_from[type].append(item['From'] + '\\' + file)
            for type in sorted_to:
                sorted_to[type].sort(key=os.path.getmtime)
            for type in sorted_from:
                sorted_from[type].sort(key=os.path.getmtime)
            for type in item['Type']:
                for file_to in sorted_to[type]:
                    for file_from in sorted_from[type]:
                        if file_from.split('\\')[-1] == file_to.split('\\')[-1]:
                            if os.path.getmtime(file_from) > os.path.getmtime(file_to):
                                os.remove(file_to)
                                shutil.copyfile(file_from, item['To'] + '\\' + file_from.split('\\')[-1])
                                print('COPIER INFO : Replace Successfully.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
                my_to = list(map(lambda x: x.split('\\')[-1], sorted_to[type]))
                my_from = list(map(lambda x: x.split('\\')[-1], sorted_from[type]))
                for form in my_from:
                    if form not in my_to:
                        if len(my_to) == item['Count']:
                            if not (os.path.getmtime(item['From'] + '\\' + form) < os.path.getmtime(item['To'] + '\\' + my_to[0])):
                                os.remove(item['To'] + '\\' + my_to[0])
                                shutil.copyfile(item['From'] + '\\' + form, item['To'] + '\\' + form)
                                print('COPIER INFO : Copy Successfully.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
                        else:
                            shutil.copyfile(item['From'] + '\\' + form, item['To'] + '\\' + form)
                            print('COPIER INFO : Copy Successfully.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))

    def run(self):
        while True:
            yaml_list = os.listdir('config-copy')
            for file in yaml_list:
                self.__read_yaml(file)
                for i, _ in enumerate(self.__config['Order']):
                    self.__procc(i)
                    time.sleep(2)