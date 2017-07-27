#! /usr/bin/python3

import os, subprocess, sys, datetime, time
import rethinkdb as r

class Log:
    def __init__(self, location, filename):
        if os.path.isfile(os.path.join(location, filename)):
            os.remove(os.path.join(location, filename))
        self.logfile=open(os.path.join(location, filename), "w")
        self.console=sys.stdout
        self.error=sys.stderr
        self.console.write("Initialized Log")

    def close(self):
        close(logfile)

    def log(self,message,level='info'):
        output='['+str(datetime.datetime.now())+'] ['+level.upper()+'] '+str(message)
        self.logfile.write(output)
        if level == "error":
            self.error.write(output)
        else:
            self.console.write(output)




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
    print(cfg)
    return cfg

def startDatabase(cfg, cwd):
    print("Starting database")
    if 'use_database' not in cfg:
        return -1
    if cfg['use_database'] == "False":
        db = subprocess.Popen(os.path.join(cwd,"rethinkdb.exe"), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        conn = None
        while conn is None:
            conn = r.connect('localhost', 28015)
        return db,conn
    else:
        pass
        #Load connection to database.

def stopDatabase(databaseObj, connection):
    connection.close()
    if isinstance(databaseObj, subprocess.Popen):
        databaseObj.terminate()

def main():

    ##############################
    # INITIALIZE SERVER !
    ###############################
    #Set variables used throughout server.
    filename='Service_Manager'
    cwd=os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    #Initialize the logger.
    logger = Log( os.path.join(cwd, 'logs') , filename+".log") #Create the log object
    print = logger.log #Make it so that whenever we use print, it will call logger.log.

    #Load the configuration file
    cfg = getConfigs(os.path.join(cwd,filename+".cfg"))

    #Initialize the socket server


    #Start the database AND/OR the DB connection
    databaseObj, connection = startDatabase(cfg, cwd)

    #######################################
    #   SHUTDOWN SERVER !
    #######################################
    stopDatabase(databaseObj, connection)
    #stopSocketServer
    #stopLogFile





if __name__ == "__main__":
    main()
