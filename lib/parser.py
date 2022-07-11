import threading
import requests
import yaml
import pyodbc
import csv
import os
import datetime
import time

class Parser(threading.Thread):
    
    def __read_yaml(self, infile):
        self.__config = {}
        with open('config-log/' + infile, 'r') as f:
            docs = yaml.load_all(f, Loader=yaml.FullLoader)
            for doc in docs:
                self.__config = doc
        self.__config['File-Name'] = infile.replace(infile.split('.')[-1], '')
        self.check_log()
                
    def check_log(self):
        if not os.path.isdir('log'):
            os.mkdir('log')
        if not os.path.isfile('log/{name}txt'.format(name=self.__config['File-Name'])):
            open('log/{name}txt'.format(name=self.__config['File-Name']), 'w').close()
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.__config = {}
    
    def sep(self, separator):
        match separator:
            case 'n':
                return '\n'
            case 't':
                return '\t'
            case _:
                return separator
    
    def __check_log(self, data):
        data = datetime.datetime.strptime(' '.join(data), self.__config['Date-Format'])
        with open('log/{name}txt'.format(name=self.__config['File-Name']), 'r') as f:
            line = f.readline().replace('\n', '')
            if line == '':
                return True
            else:
                last_data = line.split('\t')
                last_data = datetime.datetime.strptime(' '.join(last_data), self.__config['Date-Format'])
                if data <= last_data:
                    return False
                else:
                    return True
    
    def __update_log(self, data):
        open('log/{name}txt'.format(name=self.__config['File-Name']), 'w').close()
        open('log/{name}txt'.format(name=self.__config['File-Name']), 'a').write('\t'.join(data)).close()
    
    def send_data(self, result, check):
        if self.__config['Send-Type'] == 'api':
            try:
                req = requests.post(url=self.__config['Send-API'], data=result)
            except:
                print('PARSER ERR : Server Not Found.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
                return 0
            else:
                if req.text == '0':
                    print('PARSER INFO : Data Send Successfully.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
                    self.__update_log(check)
                else:
                    print('PARSER ERR : Data Doesn\'t Send.No Good Respond From Server!\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
                    return 0
        
        if self.__config['Send-Type'] == 'sql':
            try:
                conn = pyodbc.connect('Driver={driver};Server={sql_server};Database={sql_database};uid={sql_name};pwd={sql_pwd};Trusted_Connection=yes;'.format(driver='SQL Server' ,sql_server=self.__config['SQL-SERVER'], sql_database=self.__config['SQL-DATABASE'], sql_name=self.__config['SQL-USERNAME'], sql_pwd=self.__config['SQL-PWD']))
            except:
                print('PARSER ERR : Unable to connect to SQL Server.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
                return 0
            else:
                cursor = conn.cursor()
                sql = 'insert into {table_name} ({rows}) values ({results})'.format(table_name=self.__config['SQL-Table'], rows=','.join(self.__config['Names']), results=','.join(list(result.values())))
                try:
                    cursor.execute(sql)
                    conn.commit()
                except:
                    print('PARSER ERR : Something wrong in save data to SQL Server.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
                    return 0
                else:
                    print('PARSER INFO : Data Saved Successfully.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
    
    def __procc_txt(self):
        try:
            with open(self.__config['File'], 'r') as f:
                lines = f.readlines()
                for j in self.__config['Ignore-Row']:
                    lines.pop(j)
                for line in lines:
                    line = line.replace('\n', '')
                    if line != '':
                        datas = line.split(self.sep(self.__config['Separator']))
                        check = [datas[x] for x in self.__config['Check']]
                        if self.__check_log(check):
                            # Determine data
                            result = {}
                            for j, data in enumerate(self.__config['Data']):
                                result[self.__config['Names'][j]] = datas[data]
                            # Send data
                            send = self.send_data(result, check)
                            if send == 0:
                                break
                    time.sleep(2)
        except:
            print('PARSER ERR : File Not Found.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
    
    def __procc_csv(self):
        try:
            with open(self.__config['File'], 'r') as f:
                lines = csv.reader(f, delimiter=self.sep(self.__config['Separator']))
                for j in self.__config['Ignore-Row']:
                    lines.pop(j)
                for line in lines:
                    if len(line) != 0:
                        check = [line[x] for x in self.__config['Check']]
                        if self.__check_log(check):
                            # Determine data
                            result = {}
                            for j, data in enumerate(self.__config['Data']):
                                result[self.__config['Names'][j]] = line[data]
                            # Send data
                            send = self.send_data(result, check)
                            if send == 0:
                                break
                    time.sleep(2)
        except:
             print('PARSER ERR : File Not Found.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
    
    def __procc_mdb(self):
        MDB = self.__config['File']
        DRV = '{Microsoft Access Driver (*.mdb)}'
        PWD = 'pw'
        try:
            conn = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
            cursor = conn.cursor()
            cursor.execute('select * from {name}'.format(name=self.__config['Table-Name-MDB']))
            rows = cursor.fetchall()
            for row in rows:
                check = [row[x] for x in self.__config['Check']]
                if self.__check_log(check):
                    result = {}
                    for j, data in enumerate(self.__config['Data']):
                        result[self.__config['Names'][j]] = row[data]
                    # Send data
                    send = self.send_data(result, check)
                    if send == 0:
                        break
                time.sleep(2)
        except:
            print('PARSER ERR : File Not Found.\t({file_name})\t({date})'.format(file_name=self.__config['File-Name'], date=str(datetime.datetime.now())))
        
    def run(self):
        while True:
            yaml_list = os.listdir('config-log')
            for file in yaml_list:
                self.__read_yaml(file)
                if self.__config['Type'] == 'txt':
                    self.__procc_txt()
                if self.__config['Type'] == 'mdb':
                    self.__procc_mdb()
                if self.__config['Type'] == 'csv':
                    self.__procc_csv()
            time.sleep(5)