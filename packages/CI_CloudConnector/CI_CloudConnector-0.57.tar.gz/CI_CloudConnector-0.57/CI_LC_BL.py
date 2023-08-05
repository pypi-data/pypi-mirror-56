#remarks test
import httplib, urllib , json , requests , urllib2, logging , time, datetime ,sys, os , threading , socket, ConfigParser ,random, tzlocal, glob, fnmatch
import cpppo
from cpppo.server.enip import address, client
from datetime import datetime

# ------------- version
VER = '0.57' # save up to 1000 files
# ------------- version

TagsDefenitionFileName = 'TagsDefenition.txt'
TagsValuesFileName = '[NEW]TagsValues'
TagsValueDir = 'TagValues'
HomeDir = 'CI_LC'
GetTagsFromServerMinRateSeconds = 10
GetCloudVersionFromServerMinRateSeconds = 10
g_VerifySSL = False # True = do not allow un verified connection , False = Allow 

#config
cfg_serverAddress = ''
cfg_userName = ''
cfg_passWord = ''
cfg_maxFiles = ''
cfg_LogLevel = ''

sugestedUpdateVersion = ''
configFile = 'config.ini'
ScanRateLastRead = {}
currentToken = ''
g_connectorTypeName = ''
g_lastGetTagsFromServer = None
g_lastGetCloudVersionFromServer = None
g_app_log = None

# ============================
# General Functions
# ============================
def enum(**enums):
    return type('Enum', (), enums)

#Enum
TagStatus = enum(Invalid=10, Valid=20)

def initLog(loglevel=''):
    global VER
    global g_app_log
    try:
        if g_app_log:
            #print 'Log allready defined'
            return
        #print 'init Log'
        myLevel = logging.WARNING
        if loglevel == 'DEBUG':
           myLevel = logging.DEBUG 
        if loglevel == 'INFO':
           myLevel = logging.INFO 
        if loglevel == 'ERROR':
           myLevel = logging.ERROR
       
        #logging.basicConfig(filename='CI_CloudConnector.log',level=myLevel , format='%(asctime)s %(message)s')
        #logger = logging.getLogger()
        #logger.setLevel(myLevel)

        from logging.handlers import RotatingFileHandler
        log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
        logFile = 'CI_CloudConnector.log'
        my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                         backupCount=7, encoding=None, delay=0)
        my_handler.setFormatter(log_formatter)
        #my_handler.setLevel(myLevel)

        app_log = logging.getLogger('root')
        app_log.setLevel(myLevel)

        app_log.addHandler(my_handler)
        my_handler.doRollover()
        
        app_log.critical('===============================')
        app_log.critical('CI_CloudConnector Log Init ::' + VER)
        g_app_log = app_log
    except Exception as inst:
        print("Error in initLog ") + str(inst)

# ============================    
def readLastRowsFromLog(maxNumberOfRows=10):
    logFile = 'CI_CloudConnector.log'
    ans = []
    i = maxNumberOfRows;
    for line in reversed(open(logFile,'r').readlines()):
        #print line.rstrip()
        ans.append(line.rstrip())
        i = i - 1
        if i <= 0:
            return ans
    return ans

# ============================            
def setLogLevel(lvl):
    try:
        if str(lvl) in ['CRITICAL','ERROR','WARNING','INFO','DEBUG','NOTSET']:
            lvl = logging.getLevelName(str(lvl))

        #print 'level=' + str(lvl)
        if g_app_log:
            g_app_log.critical('Set Log Level to ' + logging.getLevelName(lvl) )           
            g_app_log.setLevel(lvl)        
    except Exception as inst:
        print("Error in setLogLevel ") + str(inst)

# ============================    
def ci_print(msg , level = ''):
    global g_app_log
    try:
        if level == 'DEBUG':
            g_app_log.debug(msg)
        elif level == 'INFO':
            g_app_log.info(msg)
        elif level == 'ERROR':
            g_app_log.error(msg)
        else:
            g_app_log.warning(msg)
            
        #print(level+"::"+msg)
    except Exception as inst:
        g_app_log.warning('Main Exception :: ' + inst)

# ============================    
def SendLogToServer(log):
    try:
        #check that request is set to max time and rows number
        send = True
        if send:
            print("send ::") + log
            ret = addCloudConnectorLog(log, datetime.now )  
    except:
        return

# ============================    
def testlog(cnt):
    for x in range(0, cnt):
        ci_print(str(x),'ERROR')

# ============================
def handleError(message,err):
    try:
        err_desc = str(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        srtMsg = message + " , " + str(err_desc) + " , " + str(exc_type) + " , " + str(fname) + " , " + str(exc_tb.tb_lineno)
        #print(message, err_desc, exc_type, fname, exc_tb.tb_lineno)
        ci_print(srtMsg,'ERROR')
    except Exception as errIgnore:
        ci_print("Error in handleError " + str(errIgnore),'ERROR')

# ============================
def updateAliveFile(timeStamp=None, pid=None):
    ret = False
    try:
        fileName = "/" + HomeDir + "/lc_pid.txt"
        #write tags to file
        data = {}
        if pid == None:
            pid = os.getpid()
        if timeStamp == None:
            timeStamp = str(datetime.now())
        
        data['pid'] = pid
        data['now'] = timeStamp
        f = open(fileName, 'w')
        json.dump(data, f)
        f.close()
        ret = True
    except Exception as inst:
        handleError("Error in updateAliveFile !! ", inst)
        
    return ret

# ============================
def getAliveFile():
    ret = None
    try:
        fileName = "/" + HomeDir + "/lc_pid.txt"
        #read alive file
        f = open(fileName, 'r')
        ret = json.load(f)
        #print 'getAliveFile file=' + str(ret)
    except Exception as inst:
        print("error in getAliveFile") + str(inst)
        handleError("Error in getAliveFile !! ", inst)
    return ret

# ============================
def checkIsAlive():
    ret = {}
    ret['isAlive'] = False
    isAliveTimeOutSeconds = 300
    try:
        ans = getAliveFile()
        pid = ans['pid']
        lastTimeStampStr = ans['now']
        
        if lastTimeStampStr == 'Started':
            #in case the machine was restarted
            ret['isAlive'] = False
            return ret
        
        #print 'lastTimeStampStr ' +lastTimeStampStr
        lastTimeStamp = datetime.strptime(lastTimeStampStr,"%Y-%m-%d %H:%M:%S.%f")
        now = datetime.now()
        diff = (now - lastTimeStamp).total_seconds()
        ret['diff'] = diff
        #print 'Diff = ' + str(diff)
        if diff <= isAliveTimeOutSeconds:
            ret['isAlive'] = True
        
    except Exception as inst:
        #print 'error in checkIsAlive ' + str(inst)
        handleError("Error in checkIsAlive !! ", inst)
    return ret
        
# ============================
def initConfig(overwrite = False):
    global cfg_serverAddress
    global cfg_userName
    global cfg_passWord
    global cfg_maxFiles
    global cfg_LogLevel
    #check if config exists
    try:
        filePath = "/" + HomeDir + "/" + configFile
        exists = os.path.exists(filePath)
        strLogLevels = ' , other options (DEBUG , INFO , WARNING , ERROR)'
        if exists == True:
            ci_print("Found config in " + filePath)
            Config = ConfigParser.ConfigParser()
            d = Config.read(filePath)
            cfg_serverAddress = Config.get("Server", "Address")
            cfg_userName = Config.get("Server", "username")
            cfg_passWord = Config.get("Server", "password")
            cfg_maxFiles = Config.get("Server", "maxFiles")
            
            if Config.has_section("Logging") & Config.has_option("Logging", "Level"):
                cfg_LogLevel = Config.get("Logging", "Level")
            initLog(cfg_LogLevel)
            #ci_print('err','ERROR')
            #ci_print('inf','INFO')
            
            ci_print("serverAddress:" + cfg_serverAddress)
            ci_print("userName:" + cfg_userName)
            ci_print("password:" + cfg_passWord)
            ci_print("maxFiles:" + cfg_maxFiles)
            ci_print("Logging Level:" + cfg_LogLevel + strLogLevels)
        if exists == False or overwrite == True:
            ci_print("config not found , creating new one in " + filePath)
            config = ConfigParser.RawConfigParser()
            config.add_section('Server')
            config.add_section('Logging')
            print("Updating CI_CloudConnector configuration,")
            print("Press enter to skip and use current value.")
            var = raw_input("Enter Server Address: F.E: https://localhost:63483 (Currently:" + cfg_serverAddress+ ")")
            if var != "":
                config.set('Server', 'Address', var)
            else:
                config.set('Server', 'Address', cfg_serverAddress)

            var = raw_input("Enter new user name: (Currently : " + cfg_userName + ")")
            if var != "":
                config.set('Server', 'username', var)
            else:
                config.set('Server', 'username', cfg_userName)

            var = raw_input("Enter password: (Currently : " + cfg_passWord + ")")
            if var != "":
                config.set('Server', 'password', var)
            else:
                config.set('Server', 'password', cfg_passWord)

            var = raw_input("Enter Max Files: (Currently : " + cfg_maxFiles + ")")
            if var != "":
                config.set('Server', 'maxFiles', var)
            else:
                config.set('Server', 'maxFiles', cfg_maxFiles)
            
            var = raw_input("Enter Logging Level: (Currently : " + cfg_LogLevel + ")" + strLogLevels)
            if var != "":
                config.set('Logging', 'Level', var)
            else:
                config.set('Logging', 'Level', cfg_LogLevel)

            with open(filePath, 'wb') as configfileTmp:
                config.write(configfileTmp)
                ci_print("Config Settings updated.")
                configfileTmp.close()
                initConfig()
    except Exception as inst:
        handleError('Error in initConfig', inst)

# ============================
def reboot():
    try:
        ci_print('About to reboot machine!!','CRITICAL')
        os.system('sudo reboot') 
    except Exception as inst:
        handleError("Error in reboot", inst)        
        
# ============================
# Cloud Functions
# ============================
def getCloudToken():
    global cfg_serverAddress
    global g_VerifySSL
    global currentToken
    token = ''
    url = ''
    try:
        if currentToken != '':
            ci_print("Token already acquired...")
            return currentToken

        ci_print("About to get token from cloud")
        host = cfg_serverAddress
        url = cfg_serverAddress + '/token'
        ci_print("url= " + url)
        response = requests.get(url,
                                data = {
                                    'grant_type' : 'password',
                                    'username' : cfg_userName ,
                                    'password' : cfg_passWord ,
                                    },
                                headers = {
                                    'User-Agent' : 'python',
                                    'Content-Type' : 'application/x-www-form-urlencoded',
                                    }, verify = g_VerifySSL)
        data = response.text

        #ci_print('Token Data:' + data)
        jsonData = json.loads(data)
        token = jsonData[u'access_token']

        if token != '':
            #print "set currentToken"
            currentToken = token
        
        ci_print("recieved Token ")# + token
    except Exception as inst:
        ci_print('URL :: ' + str(url))
        ci_print('Error getting Token :: ' + str(inst))
        token = ''
    return token

# ============================
# make http request to cloud if fails set currentToken='' so it will be initialized next time
# ============================
def ciRequest(url , data , postGet = 'get', method = '', token = ''):
    ans = {}
    ans["isOK"] = False
    global currentToken
    ansIsSucessful = False    
    try:
        #ci_print('url=' + url + ' ,postGet=' + postGet+ ' ,method=' + method)
        if token == '':
            ci_print("Skipping " + method + " - no Token")
            return ""            
        else:
            ci_print('Got Token Using Bearer auth' , "DEBUG")
            if postGet == 'post':
                response = requests.post(url,
                                        data,
                                        headers = {'Content-Type':"application/json",'Accept':'text/plain','Authorization': 'bearer %s' % token},
                                        verify = g_VerifySSL )
            else:
                response = requests.get(url,
                                        data = None,
                                        headers = {'Authorization': 'bearer %s' % token},
                                        verify = g_VerifySSL)
            ci_print('response='+str(response), "DEBUG")
            if response.status_code == 403:
                currentToken = ''
            ansIsSucessful = True            
    except Exception as err:
        ci_print('Error in ciRequest ' + method + " : " + str(err))
        currentToken = ''
        ansIsSucessful = False
        
    ans["isOK"] = ansIsSucessful
    ans["response"] = response
    return ans
        
# ============================
def setClock(newUtcDate):
    #strTime = '19/12/2016 13:53:55 +02:00'
    #unixTime = '2006-08-07 12:34:56'
    #newDate = unixTime
    #newDate = strTime
    try:
        if newUtcDate == '':
            return
        
        serverUtcTime = datetime.strptime(newUtcDate, '%Y-%m-%d %H:%M:%S')
        #print 'serverUtcTime=' + str(serverUtcTime)
        utcNow = datetime.utcnow()                
        diff = (utcNow - serverUtcTime).total_seconds()
        #print 'differencr from now=' + str(diff)
        if abs(diff) > 3:
            ci_print('setting new system time to ' + str(serverUtcTime) + '(UTC) ,Currently: ' + str(utcNow) + "(UTC)")
            os.system('sudo date --set="%s"' % newUtcDate + "+00:00")
            now = datetime.now()
            ci_print('New Local Time is ' + str(now))            

    except Exception as inst:
        handleError("Error in setClock ", inst)
        
# ============================
def getCloudVersion():
    global GetCloudVersionFromServerMinRateSeconds
    global g_lastGetCloudVersionFromServer
    global currentToken
    global VER
    
    if currentToken == '':
        currentToken = getCloudToken()    
    token = currentToken
    #initConfig()
    #token = getCloudToken()
    global sugestedUpdateVersion

    ci_print("start getCloudVersion")
    tags = None
    try:
        now = datetime.now()  
        getVersionTimePass = 0
        if g_lastGetCloudVersionFromServer:
            getVersionTimePass = (now - g_lastGetCloudVersionFromServer).total_seconds()
            
        ci_print('Last Get version from server was ' + str(getVersionTimePass) + ' seconds ago , getVersionRate=' + str(GetTagsFromServerMinRateSeconds))
        if getVersionTimePass == 0 or getVersionTimePass > GetCloudVersionFromServerMinRateSeconds :
            #print "update pid file for watchdog"
            #do after clock settings because some times the machine loads with old clock and trigger watchdog 
            updateAliveFile()
            
            #print "handleNewRequests"
            handleNewRequests()

            #print 'getting version from server'
            g_lastGetCloudVersionFromServer = datetime.now() 
            IpAddress = socket.gethostbyname(socket.gethostname())
            url = cfg_serverAddress + '/api/CloudConnector/GetVersion/?version=' + VER + '&IpAddress=' + IpAddress
            
            ret = ciRequest(url , None , 'get', 'getCloudVersion', token)
            response = ret["response"]            
            if ret["isOK"] == False:
                return ""  

            ci_print('gettags response=' + response.text)
            ans = json.loads(response.text)
            updateToVersion = ans[0]
            serverTime = ans[1]
            setClock(serverTime)

            sugestedUpdateVersion = updateToVersion
            if (bool(updateToVersion != '') & bool(updateToVersion != VER)):
                ci_print('! > Local Version : ' + str(VER) + ' But Server suggest Other Version : ' + str(updateToVersion))        

        #printTags(tags)
    except Exception as err:
        print(str(err))
        handleError("Error getting Version from cloud", err)
        sugestedUpdateVersion = ""
        
    return sugestedUpdateVersion

# ============================
def getCloudTags(token=''):
    global g_lastGetTagsFromServer
    global GetTagsFromServerMinRateSeconds
    #initConfig()
    #token = getCloudToken()
    ci_print("start getCloudTags")
    tags= None
    try:        
        IpAddress = socket.gethostbyname(socket.gethostname())
        url = cfg_serverAddress + '/api/CloudConnector/GetTags/'
        #ci_print(token)
        print("==") + token
        tags = None
        
        now = datetime.now()  
        getTagsTimePass = 0
        if g_lastGetTagsFromServer:
            getTagsTimePass = (now - g_lastGetTagsFromServer).total_seconds()

        #print 'getTagsTimePass='+ str(getTagsTimePass)
        ci_print('Last Get tags from server was ' + str(getTagsTimePass) + ' seconds ago , getTagsRate=' + str(GetTagsFromServerMinRateSeconds))
        if getTagsTimePass == 0 or getTagsTimePass > GetTagsFromServerMinRateSeconds :
            ret = ciRequest(url , None , 'get', 'getCloudTags', token)            
            if ret and ret["isOK"] == True:
                response = ret["response"]
                #print 'getting tags from server'
                g_lastGetTagsFromServer = datetime.now()       
                #ci_print('gettags response=' + response.text)
                ans = json.loads(response.text)
                #g_connectorTypeName = ans["connectorTypeName"]
                #printTags(ans["Tags"])
                arangedTags = arrangeTagsByScanTime(ans["Tags"])
                tags = {}
                tags["Tags"] = arangedTags
                tags["connectorTypeName"] = ans["connectorTypeName"]
                tags["PlcIpAddress"] = ans["PlcIpAddress"]
                #write tags to file
                f = open(TagsDefenitionFileName, 'w')
                json.dump(tags, f)
                f.close()
                
                ci_print("Get Cloud Counters recieved " + str(len(arangedTags)) + " Tags")
            else:
                ci_print("Get Cloud Counters from server failed ","WARNING")
    except Exception as inst:
        print(str(inst))
        handleError("Error getting tags from cloud", inst)
        tags = None
        
    if tags == None:
        tags = getTagsDefenitionFromFile()
        
    ci_print(str(tags), "INFO")
    return tags

# ============================
def arrangeTagsByScanTime(tags):
    ans={}
    try:
        ci_print("arrangeTagsByScanTime")
        
        for index in range(len(tags)):
            scanRate = tags[index][u'ScanRate']
            #ci_print("scanRate=" + str(scanRate))
            if scanRate in ans:
                tagsListPerScanRate = ans[scanRate]
            else:
                ans[scanRate]=[]

            #ci_print(ans[scanRate])
            ans[scanRate].append(tags[index])
    except Exception as err:
        handleError("arrangeTagsByScanTime", err)
    #ci_print(ans)
    return ans

# ============================
def printTags(tags):
    try:
        ci_print("Print Tags : List Contains " + str(len(tags)) + " Tags")
        ci_print(str(tags))
        for index in range(len(tags)):
            msg = 'Tag Id: ' + str(tags[index][u'TagId']) + ' ,TagName: ' + str(tags[index][u'TagName']) + ' ,TagAddress: '+ str(tags[index][u'TagAddress'])
            msg = msg + ' ,ScanRate: '+ str(tags[index][u'ScanRate'])
            ci_print(msg)
            #print 'CounterId : ' + str(tags[index])
    except Exception as inst:
        handleError("Error in printTags", inst)
        
# ============================        
def setCloudTags(tagValues , token=''):
    global TagStatus
    ci_print("start setCloudTags")
    updatedSuccessfully = False
    try:
        #url = HTTP_PREFIX + '://'+cfg_serverAddress+'/api/CloudConnector/SetCounterHistory/'
        url = cfg_serverAddress + '/api/CloudConnector/SetCounterHistory/'
        
        payload = []
        for index in range(len(tagValues)):            
            TagId = tagValues[index][u'TagId']            
            timeStamp = str(tagValues[index][u'time'])

            value = tagValues[index][u'value']
            status = TagStatus.Invalid 
            if str(tagValues[index][u'status']) == "20":
                status = TagStatus.Valid 
            #print "tagValues[index][u'status']" + str(tagValues[index][u'status'])
            ci_print('TagId = ' + str(TagId) + ' : ' + str(value))

            #{"TagId":5,"Value":"8.2","TimeStmp":"2016-06-21 11:25:56","StatusCE":""}
            tagVal = {
                'TagId':TagId
                 ,'TimeStmp':timeStamp
                 ,'StatusCE':status
                 ,'Value':value
                 }
            payload.append(tagVal)
                
        ci_print(str(payload))
        ret = ciRequest(url , json.dumps(payload) , 'post', 'setCloudTags', token)
        response = ret["response"]            
        #if token=='':
        #    ci_print("Skipping setCloudTags - no Token")
        #    return False
        #else:
        #    ci_print('Got Token Using Bearer auth')
        #    response = requests.post(url,
        #                             data = json.dumps(payload),
        #                             headers={'Content-Type':"application/json",'Accept':'text/plain','Authorization': 'bearer %s' % token})

        ci_print(response.text)
        #logging.info('setCloudTags response = ' + str(response) + ' : ' + response.text )
        #print '==' + str(response.status_code)
        updatedSuccessfully = response.status_code == 200

    except Exception as inst:
        handleError("Error setting tags in cloud", inst)
        return False

    return updatedSuccessfully

# ============================
def sendLogFileToCloud(numberOfRows = 10, timestamp = '', requestId=''):
    try:
        requestId = str(requestId)
        lines = readLastRowsFromLog(numberOfRows)
        for line in lines:
            #print "line:" + line
            addCloudConnectorLog(line , timestamp , str(requestId));
    except Exception as inst:
        print("Exception in sendLogFileToCloud ") + str(inst)
        handleError("Error setting tags in cloud", inst)
        return False
    
# ============================    
def addCloudConnectorLog(log, timeStamp = '' , requestId='' ):
    global currentToken
    if timeStamp == '':
        timeStamp = datetime.now()
    updatedSuccessfully = False

    token = currentToken
    if token == '':
        print("no token skip addCloudConnectorLog")
        return
    try:
        #url = HTTP_PREFIX + '://'+cfg_serverAddress+'/api/CloudConnector/SetCounterHistory/'
        url = cfg_serverAddress + '/api/CloudConnector/SetCounterLog/'
        
        payload = []
        logData = {
                'Log':log
                 ,'TimeStamp':str(timeStamp)
                 ,'RequestId':requestId
                 }
        payload.append(logData)
        #print str(payload)        
        ret = ciRequest(url , json.dumps(payload) , 'post', 'SetConnectorLog', token)
        response = ret["response"]

        #print (response.text)
        #logging.info('setCloudTags response = ' + str(response) + ' : ' + response.text )
        #print '==' + str(response.status_code)
        updatedSuccessfully = response.status_code == 200

    except Exception as inst:
        print("Exception in addCloudConnectorLog") + str(inst)
        #handleError("Error setting tags in cloud", inst)
        return False

    return updatedSuccessfully

# ============================
def getCloudConnectorRequests():
    global currentToken
    token = currentToken
    
    ci_print("start getCloudConnectorRequests", "INFO")
    ans = None
    try:        
        url = cfg_serverAddress + '/api/CloudConnector/GetCloudConnectorRequests/'
        ret = ciRequest(url , None , 'get', 'GetCloudConnectorRequests', token)
        #print "ret=" + str(ret)
        response = ret["response"]
        if ret["isOK"] == True:
            ans = json.loads(response.text)
    except Exception as inst:
        handleError("Error getting requests from cloud", inst)
        ans = None

    ci_print("Requests = " + str(ans), "INFO")
    return ans

# ============================    
def updateCloudConnectorRequests(requestId , status ):
    global currentToken
    updatedSuccessfully = False

    token = currentToken
    if token == '':
        print("no token skip updateCloudConnectorRequests")
        return
    try:
        #url = HTTP_PREFIX + '://'+cfg_serverAddress+'/api/CloudConnector/SetCounterRequestStatus/'
        url = cfg_serverAddress + '/api/CloudConnector/SetCounterRequestStatus/?requestId=' + str(requestId) + '&status=' + str(status)
        #print "url="+url
        ret = ciRequest(url , '' , 'post', 'SetCounterRequestStatus', token)
        response = ret["response"]

        print (response.text)
        #logging.info('setCloudTags response = ' + str(response) + ' : ' + response.text )
        #print '==' + str(response.status_code)
        updatedSuccessfully = response.status_code == 200

    except Exception as inst:
        print("Exception in addCloudConnectorLog") + str(inst)
        #handleError("Error setting tags in cloud", inst)
        return False

    return updatedSuccessfully

# get requests from cloud and handle it
# ============================ 
def handleNewRequests():    
    try:
        ci_print("start handleNewRequests","INFO")
        requests = getCloudConnectorRequests()
        if requests:
            ci_print("Got "+ str(len(requests)) + " new requests","DEBUG")
            #print "requests::" + str(requests)
            
        for request in requests:
            try:
                #print 'request[Type]=' + str(request['Type'])
                if request['Type'] == 1: # send logs
                    #print "Handling request " + str(request)
                    requestData = json.loads(request['Data'])
                    rownCount = requestData['Rows']
                    ret = updateCloudConnectorRequests(request['Id'], 2) # in process
                    requestData = json.loads(request['Data'])
                    #print "--------request['Id']===" + str(request['Id'])
                    sendLogFileToCloud(rownCount,'', request['Id'])
                    ret = updateCloudConnectorRequests(request['Id'], 3) # Done
                if request['Type'] == 2: # change logs level
                    ci_print("Handling change log level request " + str(request), "INFO")
                    requestData = json.loads(request['Data'])
                    newLogLevel = requestData['Level']
                    ret = updateCloudConnectorRequests(request['Id'], 2) # in process
                    setLogLevel(newLogLevel)              
                    ret = updateCloudConnectorRequests(request['Id'], 3) # Done
                if request['Type'] == 3: # reboot
                    ci_print("Handling reboot request " + str(request),"INFO")
                    ret = updateCloudConnectorRequests(request['Id'], 3) # Done
                    reboot()
            except Exception as innerinst:
                print("error handling request ") + str(innerinst)
                handleError("Error setting tags in inner handleNewRequests", innerinst)
    except Exception as inst:
        handleError("Error in handleNewRequests", inst)
        return False
    

# ============================
# PLC Functions
# ============================
def fill_Invalids(tagsDefenitions,values):
    global TagStatus
    
    retValues = []
    try:
        time = str(datetime.now(tzlocal.get_localzone()))
        valuesDict = {}
        ci_print("start fill_Invalids","INFO")
        # prepare values dictionery
        for val in values:
            #print "val" + str(val)
            #print "val[u'TagId']=" + str(val[u'TagId'])
            valuesDict[val[u'TagId']] = val
        #print "valuesDict="+str(valuesDict)
        for tagdef in tagsDefenitions:
            TagId = tagdef[u'TagId']
            #print "tagdef" + str(tagdef)
            if TagId in valuesDict:
                retValues.append(valuesDict[TagId])
            else:
                tagAddress = tagdef[u'TagAddress']
                val= {'TagAddress':tagAddress,'TagId':TagId,'time': time, 'value': None, 'status':TagStatus.Invalid}
                retValues.append(val)
        #print "=============="
        #print str(retValues)
    except Exception as inst:
        handleError("Error in fill_Invalids", inst)

    return retValues
    
#ippp
# ============================ 
def readEtherNetIP_Tags(tagsDefenitions, plcAddress):
    global TagStatus
    ci_print("start readEtherNetIP_Tags From " + str(plcAddress), "INFO")
    ans = []    
    try:
        tags=[]
        for index in range(len(tagsDefenitions)):
            try:
                tagAddress = tagsDefenitions[index][u'TagAddress']
                #print "tagAddress" + str(tagAddress)
                tags.append(tagAddress)
            except ValueError:
                handleError("Error reading tag address", ValueError)

        ci_print("Read tags " + str(tags), "DEBUG")
        #print 'tags = ' + str(tags)
        #tags = ["MACHINE[1].RUNNINGSIGNAL","MACHINE[1].RATE","Data_Array[0]"]
        host                        = plcAddress    # Controller IP address
        port                        = address[1]    # default is port 44818
        depth                       = 1             # Allow 1 transaction in-flight
        multiple                    = 0             # Don't use Multiple Service Packet
        fragment                    = False         # Don't force Read/Write Tag Fragmented
        timeout                     = 1.0           # Any PLC I/O fails if it takes > 1s
        printing                    = False         # Print a summary of I/O
        #tags                        = ["Data_Array[0]","Data_Array[1]"]
        #tags                        = ["Tag[0-9]+16=(DINT)4,5,6,7,8,9", "@0x2/1/1", "Tag[3-5]"]
        with client.connector( host=host, port=port, timeout=timeout ) as connection:
            operations              = client.parse_operations( tags )
            failures,transactions   = connection.process(
                operations=operations, depth=depth, multiple=multiple,
                fragment=fragment, printing=printing, timeout=timeout )

        ci_print("transactions " + str(transactions))
        ci_print("failures " + str(failures))
        #client.close()
        #sys.exit( 1 if failures else 0 )
        for index in range(len(tagsDefenitions)):
            try:
                tagAddress = tagsDefenitions[index][u'TagAddress']
                if transactions[index]:
                    TagId = int(tagsDefenitions[index][u'TagId'])
                    value = transactions[index][0]                
                    time = str(datetime.now(tzlocal.get_localzone()))

                    ci_print('get register tagAddress=' + str(tagAddress) + ' value=' + str(value))
                    val= {'TagAddress':tagAddress,'TagId':TagId,'time': time, 'value': value, 'status':TagStatus.Valid}
                    ans.append(val)
                else:
                    ci_print('Error reading Tag ' + tagAddress)
            except ValueError:
                handleError("Error reading tag value " + tagsDefenitions[index][u'TagAddress'], ValueError)
                
        ci_print("End Read readEtherNetIP Tag")
    except Exception as inst:
        handleError("Error in readEtherNetIP_Tags", inst)

    return fill_Invalids(tagsDefenitions,ans)

# ============================   
def readModBusTags(tagsDefenitions, plcAddress):
    ans = []    
    try:       
        maxOffset = 0
        for index in range(len(tagsDefenitions)):
            offset = int(tagsDefenitions[index][u'TagAddress'])
            maxOffset = max(maxOffset,offset)    
        
        ci_print("Start Read ModBus Tag")
        from pymodbus.client.sync import ModbusTcpClient as ModbusClient
        client = ModbusClient(plcAddress, port=502)
        client.connect()

        #rr = client.read_holding_registers(1,1+maxOffset) # 40000
        rr = client.read_input_registers(0,maxOffset) # 30000
        ci_print(str(rr.registers))
        for index in range(len(tagsDefenitions)):
            try:
                offset = int(tagsDefenitions[index][u'TagAddress']) - 1
                TagId = int(tagsDefenitions[index][u'TagId'])
              
                value = rr.registers[offset]
                time = str(datetime.now(tzlocal.get_localzone())) 
                ci_print("get register offset=" + str(offset) + ' value=' + str(value))
                val= {'TagAddress':offset,'TagId':TagId,'time': time, 'value': value, 'status':TagStatus.Valid}
                ans.append(val)
                #ans.update({offset:[offset,CounterId,datetime.now(),value]})
            except ValueError:
                ci_print("Error reading tag value " + tagsDefenitions[index][u'TagAddress'], "DEBUG")
        
        client.close()
        ci_print("End Read ModBus Tag")
        return ans
    except Exception as inst:
        handleError("error reading modbus", inst)
        return fill_Invalids(tagsDefenitions,ans)

# ============================
def readSimulation_Tags(tagsDefenitions):
    ci_print("start readSimulation_Tags")
    ans = []    
    try:
        for index in range(len(tagsDefenitions)):
            try:
                TagId = int(tagsDefenitions[index][u'TagId'])
                value = random.uniform(-10, 10);
                time = str(datetime.now(tzlocal.get_localzone()))
                #ci_print('get register offset=' + str(offset) + ' value=' + str(value))
                val= {'TagId':TagId,'time': time, 'value': value, 'status':TagStatus.Valid}
                ans.append(val)
            except ValueError:
                ci_print('ValueError error ')
                
        ci_print("End Read readSimulation_Tags")
        return ans
    except Exception as inst:
        handleError("error reading readSimulation", inst)
        return ans

# ============================  
def printTagValues(tagValues):
    ci_print("Count " + str(len(tagValues)) + " Tags")
    for index in range(len(tagValues)):
        ci_print(str(tagValues[index]))

# ============================      
def getLocalVersion():
    return VER

# ============================ 
def getServerSugestedVersion():
    return sugestedUpdateVersion

# ============================
# Tag Files Functions
# ============================
def writeTagsDefenitionToFile(tags):
    try:
        ci_print('Start writeTagsDefenitionToFile')  
        f = open(TagsDefenitionFileName, 'w')
        json.dump(tags, f)
        f.close()
        return 
    except Exception as inst:
        handleError("Error in writeTagsDefenitionToFile", inst)

# ============================ 
def getTagsDefenitionFromFile():
    try:
        ci_print('Start getTagsDefenitionFromFile')  
        f2 = open(TagsDefenitionFileName, 'r')
        tags = json.load(f2)
        f2.close()
        ci_print("Got " + str(len(tags)) + " Tags From File")
        #print tags
        return tags
    except Exception as inst:
        handleError("Error in getTagsDefenitionFromFile", inst)

# ============================ 
def delTagsDefenitionFile():
    try:
        ci_print('Start delTagsDefenitionFile') 
        os.remove(TagsDefenitionFileName)
        return 
    except Exception as inst:
        handleError("Error in delTagsDefenitionFile", inst)

# ============================ 
def getTagsValuesFromFile(fileName):
    try:
        ci_print('Start get Values From File ' + fileName ) 
        f2 = open(fileName, 'r')
        vals = json.load(f2)
        f2.close()
        ci_print("Got " + str(len(vals)) + " Values From File ")      
        return vals
    except Exception as inst:
        handleError("Error in getTagsValuesFromFile", inst)

# ============================ 
def saveValuesToFile(values , fileName):
    try:
        numOfFiles = len(fnmatch.filter(os.listdir("/" + HomeDir + "/" + TagsValueDir), '*.txt'))
        ci_print('Number of files in folder : ' + str(numOfFiles))
        if numOfFiles < 1000:
            if fileName == '':
                fileName = TagsValuesFileName + datetime.now().strftime("%Y%m%d-%H%M%S%f")+ '.txt'
            #fileName = "./" + TagsValueDir + '/' + fileName
            fileName = "/" + HomeDir + "/" + TagsValueDir + '/' + fileName
            ci_print('Start save Values To File ' + fileName ) 
            #write tags to file
            f = open(fileName, 'w')
            json.dump(values, f)
            f.close()
            time.sleep(1) # prevent two files in same ms
        else:
            ci_print('Too many files in folder!!!')
    except Exception as inst:
        handleError("Error in saveValuesToFile", inst)

# ============================    
def handleValuesFile(fileName, token=''):
    try:
        ci_print("Start handleValuesFile " + fileName, "INFO")
        values = getTagsValuesFromFile(fileName)
        isOk = setCloudTags(values,token)
        if isOk :
            os.remove(fileName)
            ci_print("file removed " + fileName, "INFO")
            return True
        else:
            #errFile = replaceFileName(fileName,"ERR")
            errFile = fileName.replace("/[NEW]","/ERR/[ERR]")
            os.rename(fileName, errFile)
            ci_print('Error Handling File ' + errFile, "WARNING")
    except Exception as inst:
        handleError("Error in handleValuesFile", inst)
    return False  

# ============================ 
def handleAllValuesFiles(token=''):
    try:
        ci_print('Started handleAllValuesFiles', "INFO")
        #if token=='':
        #    token = getCloudToken()
        i = 0
        dirpath = "/" + HomeDir + "/" + TagsValueDir + "/"
        filesSortedByTime = [s for s in os.listdir(dirpath)
            if os.path.isfile(os.path.join(dirpath, s))]
        filesSortedByTime.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
        ci_print('in Dir ' + dirpath + " Found " + str(len(filesSortedByTime)) + " files", "INFO")
        for file in filesSortedByTime:
            if file.endswith(".txt") and file.startswith('[NEW]'):
                i = i + 1
                ci_print('about to process file:' + file, "INFO")
                handleValuesFile("/" + HomeDir + "/" + TagsValueDir + '/' + file, token)
        
        if i > 0:
            ci_print(str(i) + ' Files handled')
    except Exception as inst:
        ci_print("Error handleAllValuesFiles " + str(inst))

# ============================ 
def createLibIfMissing():
    try:
        dirName = "/" + HomeDir + "/"
        d = os.path.dirname(dirName)
        if not os.path.exists(d):
            os.makedirs(dirName)
            ci_print('Home DIR  Created :: ' + dirName)
            
        dirName = "/" + HomeDir + "/" + TagsValueDir + "/"
        d = os.path.dirname(dirName)
        if not os.path.exists(d):
            os.makedirs(dirName)
            ci_print('TagsValueDir Created')

        dirName = "/" + HomeDir + "/" + TagsValueDir + "/ERR/"
        d = os.path.dirname(dirName)
        if not os.path.exists(d):
            os.makedirs(dirName)
            ci_print('TagsValueDir/ERR Created')
            
    except Exception as inst:
        ci_print("Error createLibIfMissing " + str(inst))        

# ============================ 
# Test
def Test():
    try: 
        print("Test Process")
        token = getCloudToken()
        if token and len(token) > 0:
            print("---------------")
            print("Got Token")
            tagsDefScanRatesAns = getCloudTags(currentToken)
            if tagsDefScanRatesAns and len(tagsDefScanRatesAns)>0:
                print("---------------")
                print("Got Tags Defenitions")
                print(str(tagsDefScanRatesAns))
                plcMode = tagsDefScanRatesAns["connectorTypeName"]
                tagsDefScanRates = tagsDefScanRatesAns["Tags"]
                plcAddress = tagsDefScanRatesAns["PlcIpAddress"]            
                
                for scanRate in tagsDefScanRates:
                    print("For Scan rate") + str(scanRate)
                    tagsDef = tagsDefScanRates[scanRate]
                    
                    values = readEtherNetIP_Tags(tagsDef, plcAddress)
                    if values and len(values)>0:
                        print("---------------")
                        print("Got Values from PLC")
                        print(str(values))
                    else:
                        print("Could not get values from PLC")
            else:
                print("Could not get tags defenition from server")  
        else:
            print("Could not get login login token, check config for server defenition")
    except Exception as err:
        err_desc = str(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        srtMsg = message + " , " + str(err_desc) + " , " + str(exc_type) + " , " + str(fname) + " , " + str(exc_tb.tb_lineno)
        #print(message, err_desc, exc_type, fname, exc_tb.tb_lineno)
        print(srtMsg)

# ============================
# Remove oldest file
# ============================
def removeOldestFile():
    global cfg_maxFiles

    try:
        dirName = "/" + HomeDir + "/" + TagsValueDir + "/"
        dir = os.path.dirname(dirName)
        if os.path.exists(dir):    
            list_of_files = glob.glob(dirName + '*.txt')
            num_of_files = len(list_of_files)
            maxFiles = int(cfg_maxFiles)

            if maxFiles < num_of_files & num_of_files > 0:
                # In case more than one file is exceeding cfg_maxFiles. 
                # Used for initial case where num of files is much bigger than config MaxFiles.
                for x in range(maxFiles, num_of_files):
                    oldest_file = min(list_of_files, key=os.path.getctime)
                    os.remove(oldest_file)
                    list_of_files.remove(oldest_file)

    except Exception as inst:
        handleError("Error in removeOldestFile", inst)
        
# ============================
# Main Loop 
# ============================ 
def Main():
    global ScanRateLastRead
    global currentToken
    try:    
        ci_print('Loop started at ' + str(datetime.now()))
        if (currentToken == ''):
            currentToken = getCloudToken()
        # currently must get tags from cloud to init server before setting values
        tagsDefScanRatesAns = getCloudTags(currentToken)
        plcMode = tagsDefScanRatesAns["connectorTypeName"]
        tagsDefScanRates = tagsDefScanRatesAns["Tags"]
        plcAddress = tagsDefScanRatesAns["PlcIpAddress"]
        
        for scanRate in tagsDefScanRates:
            scanRateInt = int(scanRate)
            scanRateStr = str(scanRate)
            diff = 0
            if scanRateStr in ScanRateLastRead:
                now = datetime.now()                
                diff = (now - ScanRateLastRead[scanRateStr]).total_seconds()
                #print ('diff = -------' + str(diff))

            ci_print('*********************','INFO')
            ci_print('diff=' + str(diff) + ' scanRateInt=' + str(scanRateInt),'INFO')
            print('diff='+str(diff) + ' scanRateInt=' + str(scanRateInt))
            if diff + 3 > scanRateInt or diff == 0:
                ci_print("Get Tag Values For Scan Rate " + str(scanRate) + " ' time Form Last Run:" + str(diff) + " Sec")
                tagsDef = tagsDefScanRates[scanRate]
                #printTags(tagsDef)
                values = None
                if plcMode == 'Simulation':
                    values = readSimulation_Tags(tagsDef) 
                if plcMode == 'Modbus':
                    values = readModBusTags(tagsDef, plcAddress)
                if plcMode == 'Ethernet/IP':
                    values = readEtherNetIP_Tags(tagsDef, plcAddress)
                    if values == []:
                        ci_print("Ethernet Empty values ::1",'ERROR') 
                        values = readEtherNetIP_Tags(tagsDef, plcAddress)
                        if values == []:
                            time.sleep(0.1) # wait before try to reat values again
                            ci_print("Ethernet Empty values ::2",'ERROR') 
                            values = readEtherNetIP_Tags(tagsDef, plcAddress)
                            if values == []:
                                time.sleep(1) # wait before try to reat values again
                                ci_print("Ethernet Empty values ::3",'ERROR') 
                                values = readEtherNetIP_Tags(tagsDef, plcAddress)
                    

                if len(values) > 0:
                    printVal = " Val=" + str(values[0]["value"]) + " " + str( len(values)) + " Tags"
                    ci_print(printVal) 
                    print (str(datetime.now()) + ' Send Vals:' + str(scanRate) + " diff " + str(diff) + printVal)
                else:
                    printVal = " No Values"
                    ci_print(printVal,'ERROR') 
                    print (str(datetime.now()) + ' Send Vals:' + str(scanRate) + " diff " + str(diff) + printVal)
                
                #printTagValues(values)
                if values:
                    saveValuesToFile(values,'')                    
                    removeOldestFile()

                    now = datetime.now()
                    ci_print('scanRateStr time updated==>' + str(now)) 
                    ScanRateLastRead[scanRateStr] = now
        if currentToken != '':
            handleAllValuesFiles(currentToken)
        else:
            ci_print("No Token, skipping upload step")
    except Exception as inst:
        handleError("Error in Main", inst)     
        currentToken = ''

    ci_print('===============================')
    ci_print('CI_CloudConnector Ended')

initLog()
initConfig()
#Main()
