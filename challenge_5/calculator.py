#!/usr/bin/env python3
import sys
import csv
from multiprocessing import Process,Queue

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
        index = self.args.index('-c')
        self.configfile = self.args[index+1]
        dindex = self.args.index('-d')
        self.userdatafile = self.args[dindex+1]
        oindex = self.args.index('-o')
        self.outputfile = self.args[oindex+1]

class Config(object):
    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config = {}
        args = Args()
        with open(args.configfile,'r') as f:
            for line in f.readlines():
                l = line.strip().split('=')
                con_key = l[0].strip()
                con_value = l[1].strip()
                config[con_key] = con_value
        return config

    


class UserData(object):
    def __init__(self):
        pass
    def _read_users_data(self,q):
        userdata = {}
        args = Args()
        with open(args.userdatafile,'r') as f:
            for line in f.readlines():
                l = line.strip().split(',')
                con_key = l[0].strip()
                con_value = l[1].strip()
                userdata[con_key] = con_value
        q.put(userdata)
        print('send data:{}'.format(userdata))

    


class IncomeTaxCalculator(object):

    def calc_for_all_userdata(self,q1,q2):
        result = []
        tax = 0
        should_tax = 0
        social_insurance = 0

        conf = Config()
        config = conf.config
        JiShuL = float(config['JiShuL'])
        JiShuH = float(config['JiShuH'])
        YangLao = float(config['YangLao'])
        YiLiao = float(config['YiLiao'])
        ShiYe = float(config['ShiYe'])
        GongJiJin = float(config['GongJiJin'])
        userdata = q1.get()
        print('receive data:{}'.format(userdata))
        for id,salary in userdata.items():
            salary = float(salary)
            if salary > 0 and salary < JiShuL:
                social_insurance = JiShuL * (YangLao + YiLiao + ShiYe + GongJiJin)
            elif salary > JiShuH:
                social_insurance = JiShuH * (YangLao + YiLiao + ShiYe + GongJiJin)
            else:
                social_insurance = salary * (YangLao + YiLiao + ShiYe + GongJiJin)

            should_tax = salary - social_insurance - 5000
               
            if should_tax > 0 and should_tax <= 3000:
                tax = should_tax * 0.03
            elif should_tax > 3000 and should_tax <= 12000:
                tax = should_tax * 0.1 - 210 
            elif should_tax > 12000 and should_tax <= 25000:
                tax = should_tax * 0.2 - 1410 
            elif should_tax > 25000 and should_tax <= 35000:
                tax = should_tax * 0.25 - 2660 
            elif should_tax > 35000 and should_tax <= 55000:
                tax = should_tax * 0.3 - 4410 
            elif should_tax > 55000 and should_tax <= 80000:
                tax = should_tax * 0.35 - 7160
            elif salary > 80000:
                tax = should_tax * 0.45 - 15160
           
            final_salary = salary - social_insurance - tax

            result.append([id,salary,'{:.2f}'.format(social_insurance),'{:.2f}'.format(tax),'{:.2f}'.format(final_salary)])
        q2.put(result)
        


    def dumptofile(self,q2):
        result = q2.get()
        args = Args()
        with open(args.outputfile,'a') as f:
            writer = csv.writer(f)
            writer.writerows(result)

    

if __name__ == '__main__':
    queue1 = Queue()
    queue2 = Queue()
    userdata = UserData()
    Process(target=userdata._read_users_data,args=(queue1,)).start()
    income = IncomeTaxCalculator()
    Process(target=income.calc_for_all_userdata,args=(queue1,queue2)).start()
    Process(target=income.dumptofile,args=(queue2,)).start()





