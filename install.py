import pip, platform

git="https://github.com/Kiln707/Kilns-Server-Manager.git"
WinInstallLocation="C:\Kilns-Server-Manager"
UXInstallLocation="/Kilns-Server-Manager"

def

def installServer():
    system = platform.system()
    if system == 'Linux':
        #See if docker is installed
        try:
            # pipe output to /dev/null for silence
            null = open("/dev/null", "w")
            subprocess.Popen("docker", stdout=null, stderr=null)
            null.close()
        except OSError:
            null.close()
            #TODO: Install docker

    elif system == 'Windows':
        pass
    else:
        print("An invalid Operating System was found.")
        return -1
    pip.main(['install', "optparser"])
    pip.main(['install', "docker"])


##################################################
#   Future work. 25 July 2017
###################################################
def installConsole():
    pass

def installWebConsole():
    pass
