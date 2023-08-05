#remarks test
import threading , pip , CI_LC_BL, time , datetime , json
from datetime import datetime

import sys, logging
import cpppo
from cpppo.server.enip import address, client

upgradeCounter = 0
serverVersion = ''
threadTimer = None
watchDogThreadTimer = None
    
from threading import Timer
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def reloadLC():
    try:
        CI_LC_BL.ci_print('! About to reload', 'ERROR')
        CI_LC_BL.reboot()
        #reload(CI_LC_BL)
        #CI_LC_BL.initConfig()
    except Exception as inst:
        CI_LC_BL.handleError('reloadLC::Error ', inst)
        #print "Error reload " + str(inst)        
        #logging.warning('Error in reload :: ' + str(inst))
        
def upgradeLC(ver='', currentVer=''):
    try:
        if ver == '':
            print('! About to upgrade to latest version')
            CI_LC_BL.ci_print('! About to upgrade to latest version')
            pip.main(['install','--upgrade','CI_CloudConnector'])
        else:
            print('! About to upgrade to specific version'+ ver)
            CI_LC_BL.ci_print('! About to upgrade to specific version ' + ver)
            pip.main(['install','--force-reinstall','CI_CloudConnector=='+ver])
    except Exception as inst:
        CI_LC_BL.handleError('upgradeLC::Error ', inst)
        #print "Error upgrade " + str(inst)        
        #logging.warning('Error in upgrade :: ' + str(inst))

def watchDogLoop():
    global threadTimer
    try:
        print("watchDogLoop::Start")
        CI_LC_BL.ci_print("watchDogLoop::Start","DEBUG")
        ret = CI_LC_BL.checkIsAlive()
        isAlive = ret['isAlive']
        diff = ret['diff']
        msg = ""
        if isAlive == False:
            print("watchDogLoop::MainLoop Not Working, restarting ") + str(diff)
            CI_LC_BL.ci_print("watchDogLoop::MainLoop Not Working , restarting","CRITICAL")
            print("watchDogLoop::threadTimer = ") + str(threadTimer)
            CI_LC_BL.ci_print("watchDogLoop::threadTimer = " + str(threadTimer),"CRITICAL")
            if threadTimer:
                if diff<250:
                    CI_LC_BL.ci_print("watchDogLoop::Found threadTimer try start again, <250 ","CRITICAL")
                    threadTimer.stop()
                    threadTimer = RepeatedTimer(5, MainLoopTimer)
                    msg = "watchDogLoop::Found threadTimer try start again, <250 "
                if diff > 250 and diff < 900:
                    print("watchDogLoop:: restarting timer")
                    CI_LC_BL.ci_print("watchDogLoop::Found threadTimer but its not working, restarting timer ","CRITICAL")
                    threadTimer.stop()
                    threadTimer = RepeatedTimer(5, MainLoopTimer)
                    msg = "watchDogLoop::Found threadTimer but its not working, restarting timer "
                if diff > 900:
                    CI_LC_BL.ci_print("watchDogLoop::Found threadTimer but its not working more then 900 sec, reboot machine ","CRITICAL")
                    CI_LC_BL.reboot()
                    msg = "watchDogLoop::Found threadTimer but its not working more then 900 sec, reboot machine "
                    
                CI_LC_BL.ci_print("watchDogLoop::threadTimer.is_running = " + str(threadTimer.is_running),"CRITICAL")
            else:
                print("watchDogLoop:: No thread Timer")
                if diff > 250 and diff < 900:
                    print("watchDogLoop:: restarting timer")
                    CI_LC_BL.ci_print("watchDogLoop::No timer , restarting timer ","CRITICAL")
                    threadTimer = RepeatedTimer(5, MainLoopTimer)
                    msg = "watchDogLoop::No timer , restarting timer "
                    #CI_LC_BL.reboot()
                if diff > 900:
                    CI_LC_BL.ci_print("watchDogLoop::threadTimer not found over 900, reboot machine ","CRITICAL")
                    CI_LC_BL.reboot()
                    msg = "watchDogLoop::threadTimer not found over 900, reboot machine "
                    
            #fileName = "WatchDog_" + datetime.now().strftime("%Y%m%d-%H%M%S")+ '.txt'
            fileName = "WatchDog.log"
            f = open(fileName, 'a')
            text = str(datetime.now()) + " , offline time = " + str(diff) + " sec " + msg + "\n"
            f.write(text)
            #json.dump(str(datetime.now()), f)
            f.close()
            #CI_LC_BL.reboot()
    except Exception as inst:
        CI_LC_BL.ci_print("watchDogLoop::Error " + str(inst),"ERROR")

def MainLoopTimer():
    global threadTimer
    if threadTimer:
        threadTimer.stop()
    try:
        MainLoop()
    except Exception as inst:
        CI_LC_BL.ci_print("MainLoopTimer::Error MainLoop " + str(inst),"ERROR")    
    
    if threadTimer:
        threadTimer.start()
    else:
        CI_LC_BL.ci_print("MainLoopTimer::threadTimer not found!","ERROR")
        print("threadTimer not found!")
        threadTimer = RepeatedTimer(5, MainLoopTimer)
        CI_LC_BL.ci_print("MainLoopTimer::Starting threadTimer again!","ERROR")
        
def MainLoop():
    global serverVersion
    global upgradeCounter
    
    try: 
        # get version and update if needed
        CI_LC_BL.getCloudVersion()
        localVer = str(CI_LC_BL.getLocalVersion())
        updateToVer = str(CI_LC_BL.getServerSugestedVersion())
        #to prevent upgrading to much in case of a problem we count upgrade attempts and stop when its too big, but if the version changes we try again
        if serverVersion != updateToVer:
            serverVersion = updateToVer
            upgradeCounter = 0

        CI_LC_BL.ci_print("local ver=" + localVer)
        CI_LC_BL.ci_print("server ver= " + updateToVer)

        if str(updateToVer) == 'None':
            updateToVer=''
        if (bool(updateToVer != '') & bool(updateToVer != localVer) & bool(upgradeCounter < 10)):
            upgradeCounter = upgradeCounter + 1
            CI_LC_BL.ci_print('Local Version is different than server suggested version, start auto upgrade from:' + localVer + ' To:' + updateToVer + ' Upgrade count:'+str(upgradeCounter))
            upgradeLC(updateToVer, localVer)
            reloadLC()

        # Get Values and send to cloud
        CI_LC_BL.Main() 
    except Exception as inst:
        CI_LC_BL.ci_print("MainLoop::Error " + str(inst),"ERROR")
    
def StartMainLoop():
    global threadTimer
    try:
        CI_LC_BL.ci_print("CI_CloudConnector Started")
        CI_LC_BL.updateAliveFile("Started")
        threadTimer = RepeatedTimer(5, MainLoopTimer)
        watchDogThreadTimer = RepeatedTimer(30, watchDogLoop)
        #threadTimer = RepeatedTimer(5, test)
    except Exception as inst:
        CI_LC_BL.ci_print("StartMainLoop::Error " + str(inst))
        
def showHelp():
    print ("==============================================")
    print ("CI_CloudConnector Version: " + CI_LC_BL.getLocalVersion())
    print ('CI_CloudConnector.py :Start application')
    print ('CI_CloudConnector.py help   : display command line help')
    print ('CI_CloudConnector.py Start  : Start Main Loop')
    print ('CI_CloudConnector.py Config : UpdateConfig defenitions')
    print ("==============================================")
    print ('CI_CloudConnector.py getCloudVersion : check server suggected version and time')
    print ('CI_CloudConnector.py getCloudTags  : Get Tags defenition from Cloud and save into file')
    print ('CI_CloudConnector.py LocalDefTagsFiles : Show the tags saved in file')
    print ('CI_CloudConnector.py readModBusTags : Read Tags Fom Modbus and save to file')
    print ('CI_CloudConnector.py readEtherNetIP_Tags : Read Tags Fom EtehernatIP and save to file')
    print ('CI_CloudConnector.py handleAllValuesFiles : Send Values from all files to cloud')    
    print ('CI_CloudConnector.py TestMainLoopOnce : test main loop functionality one time')
    print ('CI_CloudConnector.py Test : Test Components')
    print ("==============================================")

def args(argv):
    #print 'Argument List:', str(argv)
    #print 'Argument List:', str(len(argv))
    #if (len(sys.argv)==1):
    #    CI_LC_BL.MainLoopStart()
    if (len(argv) > 1 and argv[1] == 'help'):
        showHelp()

    if (len(argv) > 1 and argv[1] == 'Start'):
        StartMainLoop()

    if (len(argv) > 1 and argv[1] == 'Config'):
        CI_LC_BL.initConfig(True)

    if (len(argv) > 1 and argv[1] == 'Test'):
        CI_LC_BL.Test()

    if (len(argv) > 1 and argv[1] == 'getCloudTags'):
        token = ''
        token = CI_LC_BL.getCloudToken()
        CI_LC_BL.getCloudTags(token)

    if (len(argv) > 1 and argv[1] == 'LocalDefTagsFiles'):
        tagsDef = CI_LC_BL.getTagsDefenitionFromFile()
        CI_LC_BL.printTags(tagsDef)

    if (len(argv) > 1 and argv[1] == 'readModBusTags'):
        tagsDef = getTagsDefenitionFromFile()
        #printTags(tagsDef)
        values = readModBusTags(tagsDef)
        printTagValues(values)
        saveValuesToFile(values,'')

    if (len(argv) > 1 and argv[1] == 'readEtherNetIP_Tags'):
        tagsDef = getTagsDefenitionFromFile()
        printTags(tagsDef)
        values = readEtherNetIP_Tags(tagsDef)
        printTagValues(values)
        saveValuesToFile(values,'')

    if (len(argv) > 1 and argv[1] == 'handleAllValuesFiles'):
        token = ''
        token = CI_LC_BL.getCloudToken()
        CI_LC_BL.handleAllValuesFiles(token)

    if (len(argv) > 1 and argv[1] == 'TestMainLoopOnce'):
        MainLoop()

    if (len(argv) > 1 and argv[1] == 'upgradeLC'):
        upgradeLC()

    if (len(argv) > 1 and argv[1] == 'getCloudVersion'):
        CI_LC_BL.getCloudVersion()

def menu(option='help'):
    args(["",option])
    
#handle
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#print 'Argument List:', str(sys.argv[1])
CI_LC_BL.initLog()
CI_LC_BL.createLibIfMissing()
CI_LC_BL.initConfig()

args(sys.argv)

#MainLoop()
    






