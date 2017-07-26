#! /usr/bin/python3

import sys

####################################################################################################
# Variable Section
###################################################################################################
#A note for which functions haven't been implemented yet
inDevelop="Not Implemented."
#Usage display. TODO:
usage=" Usage: "+sys.argv[0]+" COMMAND"
#Commands will need to be expanded with the switch in parseCommand()
commands=["START","STOP","RESTART","CREATE","DELETE","EDIT","EXPORT","IMPORT","BACKUP","INSTALL"]
#Options will need to be expanded with the switch in parseOptions()
options=["--help", "-h","--version", "-v"]

###################################
# Parse Command
##################################
def parseCommand(command, args):
    if command == "START":
        print("Start Service.",inDevelop, args)
    elif command == "STOP":
        print("Stop Service.",inDevelop, args)
    elif command == "RESTART":
        print("Restart Service.",inDevelop)
    elif command == "CREATE":
        print("Create Service.",inDevelop)
    elif command == "DELETE":
        print("Delete Service.",inDevelop)
    elif command == "EDIT":
        print("Edit Service.",inDevelop)
    elif command == "EXPORT":
        print("Export Service.",inDevelop)
    elif command == "IMPORT":
        print("Import Service.",inDevelop)
    elif command == "BACKUP":
        print("Backup Service.",inDevelop)
    elif command == "INSTALL":
        print("Install Server Manager.",inDevelop)

##############################
# Start script Section
##############################

arg = str(sys.argv[1]).upper()
if arg in commands:
    parseCommand(arg, sys.argv[2:])
elif arg in options:
    parseOption(arg)
else:
    print("Invalid command.\n"+usage)
