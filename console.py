#! /usr/bin/python3
from Serialization import Tag
from Serialization.json_io import encodeJSON, decodeJSON
import sys, socket, struct

####################################################################################################
# Variable Section
###################################################################################################
#A note for which functions haven't been implemented yet
inDevelop="Not Implemented."
#Usage display. TODO:
usage=" Usage: "+sys.argv[0]+" COMMAND"
#Commands will need to be expanded with the switch in parseCommand()
commands=["START","STOP","RESTART","Status","CREATE","DELETE","EDIT","LIST","EXPORT","IMPORT","BACKUP","INSTALL"]
#Options will need to be expanded with the switch in parseOptions()
options=["--help", "-h","--version", "-v"]


###############################################
#   Configuration Section
##############################################
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

###########################################
#   Networking Section
###########################################
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

###################################
# Parse Command
##################################
def parseCommand(command, args, connection):
    tag= Tag()
    tag.addData('COMMAND', command)
    tag.addData('DATA', args)
    if command == "START":
        sendNetworkData(connection, encodeJSON(tag) )
        print("Start Service.",inDevelop)
    elif command == "STOP":
        sendNetworkData(connection, "STOP")
        print("Stop Service.",inDevelop)
    elif command == "RESTART":
        print("Restart Service.",inDevelop)
    elif command == "STATUS":
        print("Service status.",inDevelop)
    elif command == "CREATE":
        print("Create Service.",inDevelop)
    elif command == "DELETE":
        print("Delete Service.",inDevelop)
    elif command == "EDIT":
        print("Edit Service.",inDevelop)
    elif command == "LIST":
        print("List Services.",inDevelop)
    elif command == "EXPORT":
        print("Export Service.",inDevelop)
    elif command == "IMPORT":
        print("Import Service.",inDevelop)
    elif command == "BACKUP":
        print("Backup Service.",inDevelop)
    elif command == "INSTALL":
        print("Install Server Manager.",inDevelop)

######################################################################################
# --------     Start script Section    --------------
######################################################################################
#Connect to Server's Console


#########################
# Command Section
#########################
arg = str(sys.argv[1]).upper() #Get the command
if arg in commands:
    serverConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverConnection.connect( ('localhost', 8889) )
    parseCommand(arg, sys.argv[2:], serverConnection)
    serverConnection.shutdown(socket.SHUT_RDWR)
    serverConnection.close()
elif arg in options:
    parseOption(arg)
else:
    print("Invalid command.\n"+usage)
