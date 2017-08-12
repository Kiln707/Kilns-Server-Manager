#! /usr/bin/python3

import os, subprocess, sys, datetime, time, socket, select, struct
import rethinkdb as r

############################################
# Log class
# Handles writing to console and log files
############################################
logger=None
class Log:
    def __init__(self, location, filename):
        global print
        if os.path.isfile(os.path.join(location, filename)):
            os.remove(os.path.join(location, filename))
        self.logfile=open(os.path.join(location, filename), "w")
        self.console=sys.stdout
        self.error=sys.stderr
        print = self.log #Make it so that whenever we use print, it will call logger.log.
        print("Initialized Log.")

    def close(self):
        self.log("Closing Logs.")
        self.logfile.close()
        self.console.close()
        self.error.close()

    def log(self,message,level='info'):
        output='['+str(datetime.datetime.now())+'] ['+level.upper()+'] '+str(message)+"\n\r"
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

################################
#   Configuration file reading
################################
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

###################################
# Networking/Console Section
###################################
def initializeNetworking(cfg):
    global logger
    print("Initialzing Network...")

    print("Initilizing Console socket...")
    consoleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        consoleSocket.bind( ('localhost', 8889) )
    except socket.error as msg:
        logger.log("Failed to bind Console. Error Code:", str(msg[0]), 'Message:',msg[1])
    consoleSocket.listen(5)
    print("Console socket intitialized.")
    if(cfg['bind_ip'] != ''):
        print("Initilizing Console socket...")
        networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            networkSocket.bind( (cfg['bind_ip'], int(cfg['bind_port'])) )
        except socket.error as msg:
            logger.log("Failed to bind to",cfg['bind_ip']+":"+cfg['bind_port'],"Error Code:", str(msg[0]), 'Message:',msg[1])
        networkSocket.listen(5)
        print("Console socket intitialized.")
    else:
        logger.log("Not accepting Network Connections!",'WARN')
    print("Network intitialization complete.")
    return networkSocket, consoleSocket

def sendNetworkData(connection, data):
    connection.sendall(struct.pack('>i', len(data))+data.encode('ascii'))

def receiveNetworkData(connection):
    #data length is packed into 4 bytes
    total_len=0;total_data=bytearray();size=sys.maxsize
    sock_data=bytearray();recv_size=8192
    while total_len<size:
        sock_data=connection.recv(recv_size)
        if not sock_data:
            return None
        if not total_data:
            if len(sock_data)>4:
                size=struct.unpack('>i', sock_data[:4])[0]
                for b in sock_data[4:]:
                    total_data.append(b)
            elif len(sock_data) == 4:
                size=struct.unpack('>i', sock_data[:4])[0]
        else:
            total_data.append(sock_data)
        total_len=len(total_data)
    return bytes(total_data).decode('ascii')

def processClientData(data):
    pass

def shutdownNetworking(consoleSocket, networkSocket):
    print("Shutting down networking...")
    consoleSocket.close()
    networkSocket.close()
    print('Network shutdown complete.')

###################################
# Database Section
##################################
def initializeDatabase(cfg, cwd):
    print("Initilizing database...")
    if 'use_database' not in cfg:
        sys.exit(-1) #Error, should not happpen
    if cfg['use_database'] == "False":
        db = subprocess.Popen(os.path.join(cwd,"rethinkdb.exe"), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        conn = None
        while conn is None:
            conn = r.connect('localhost', 28015)
        print("Database intitialization complete.")
        return db,conn
    else:
        pass
        #Load connection to database.

def queryDatabase():
    pass

def shutdownDatabase(databaseObj, connection):
    print("Shutting down database...")
    connection.close()
    if isinstance(databaseObj, subprocess.Popen):
        databaseObj.terminate()
    print('Database shutdown complete.')

######################################
#   Program Section
#####################################

def main():

    ##############################
    # INITIALIZE SERVER !
    ###############################
    #Set variables used throughout server.
    filename='Service_Manager'
    cwd=os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    global logger
    #Initialize the logger.
    logger = Log( os.path.join(cwd, 'logs') , filename+".log") #Create the log object

    #Load the configuration file
    cfg = getConfigs(os.path.join(cwd,filename+".cfg"))

    #Start the database AND/OR the DB connection
    databaseObj, connection = initializeDatabase(cfg, cwd)

    #Initialize the socket server
    consoleSocket, networkSocket = initializeNetworking(cfg)

    connectionList={}

    #######################################
    #   SERVER RUNNING !
    ######################################
    read_list = [consoleSocket, networkSocket]
    RUNNING=True
    while RUNNING:
        print("Iteration")
        readable, writable, errored = select.select(read_list, [],[], 0.5)
        for s in readable:
            if s is networkSocket:
                print("NetSocket")
                client_sock, address = networkSocket.accept()
                read_list.append(client_sock)
                connectionList[client_sock]=address
                print("Connection from"+str(address))
            elif s is consoleSocket:
                print("ConSocket")
                client_sock, address = consoleSocket.accept()
                read_list.append(client_sock)
                print("Console Connected!")
            else:
                print("OtherSock")
                data = receiveNetworkData(s)
                if data:
                    print(data)
                    if(str(data) == "STOP"):
                        RUNNING=False
                else:
                    address = connectionList[s]
                    print("Closing "+str(address) )
                    s.close()
                    connectionList.pop(s,None)
                    read_list.remove(s)

    #######################################
    #   SHUTDOWN SERVER !
    #######################################
    shutdownNetworking(consoleSocket, networkSocket) #Closing networking
    shutdownDatabase(databaseObj, connection) #Closing database
    logger.close() #Closing Logger





if __name__ == "__main__":
    main()
