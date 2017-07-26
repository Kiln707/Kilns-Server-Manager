#! /usr/bin/python3

import os, subprocess

def __charPos(char, string, pos=0):
        for i in range(pos+1, len(string)):
                if string[i] is char:
                        return i
        return -1

def getConfigs(location):
    cfg = { }
    if os.path.isfile(location): #If the configuration file exists
        cfgFile = open(location)
        line = cfgFile.readline()
        while line != '':	#until the end of the file has been reached
            delimiter=__charPos('=',line)	#If there is an =, get it's position
            if delimiter == '':
                cfg[line] = True	#If no =, it is a flag. Set the variable to True
            else:
                key = line[0:delimiter] #Get the Key name
                value = line[delimiter+1:len(line)] #Parse out the value
                if value[0] == "'" or value[0] == '"': #Remove unnecessary Quotes
                    value = value[1:]
                if value[len(value)-1] == "'" or value[len(value)-1] == '"':
                    value = value[0:len(value)-1] #End removing Unnecessary Quotes
                cfg[key] = value.replace('\n', '').replace('\t','').replace('\r','') #Set the value of the
                line = cfgFile.readline()
    return cfg

def startDatabase(cfg):
    if 'use_database' not in cfg:
        return -1
    if cfg['use_database'] == "False":
        print('start private database')


def main():
    cfg = getConfigs(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__),"Service_Manager.cfg")))
    startDatabase(cfg)





if __name__ == "__main__":
    main()
