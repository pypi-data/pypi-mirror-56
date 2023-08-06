import requests
import grequests
#from requests import async
import json
###################################
##Orchestrator integration module (safe use when orchestrator is turned off)
###################################

################################################################################
#Send data to orchestrator (asynchronyous)
#Example: t=IntegrationOrchestrator.DataSend(["Storage","Robot_R01"],{"RunDateTimeString":"Test1","StepCurrentName":"Test2","StepCurrentDuration":"Test333","SafeStopSignal":True},"localhost",8081)
def DataSend(inKeyList,inValue,inOrchestratorHost="localhost",inOrchestratorPort=80):
    lURL = f'http://{inOrchestratorHost}:{inOrchestratorPort}/ProcessingRun'
    lDataJSON = {"actionList":[{"type":"AdministrationGlobalDictSetKeyListValue","key_list":inKeyList,"value":inValue}]}  
    #lAsyncList = []
    lResultItem = [grequests.post(lURL, json=lDataJSON)]
    return grequests.map(lResultItem)    
    #lAsyncList.append(lResultItem)
    #return async.map(lAsyncList)
################################################################################
#recieve Data from orchestrator
#t=IntegrationOrchestrator.DataRecieve(["Storage","Robot_R01"],"localhost",8081)
def DataRecieve(inKeyList,inOrchestratorHost="localhost",inOrchestratorPort=80):    
    lURL = f'http://{inOrchestratorHost}:{inOrchestratorPort}/ProcessingRun'
    lDataJSON = {"actionList":[{"type":"AdministrationGlobalDictGetKeyListValue","key_list":inKeyList}]}  
    try:
        lResult = requests.post(lURL, json=lDataJSON)    
        lResultJSON = json.loads(lResult.text)
        return lResultJSON["actionListResult"][0]["value"]
    except Exception:
        return None
################################################################################
#Check if orchestrator has safe stop signal
#Example: IntegrationOrchestrator.SafeStopSignalIs(["Storage","Robot_R01","SafeStopSignal"],"localhost",8081)
def SafeStopSignalIs(inKeyList,inOrchestratorHost="localhost",inOrchestratorPort=80):
    lResult=False
    lResponse=DataRecieve(inKeyList,inOrchestratorHost,inOrchestratorPort)
    if lResponse is not None:
        lResult = lResponse
    return lResult
################################################################################
#Reset SafeStop signal in orchestrator
#Example: t=IntegrationOrchestrator.SafeStopSignalReset(["Storage","Robot_R01","SafeStopSignal"],"localhost",8081)
def SafeStopSignalReset(inKeyList,inOrchestratorHost="localhost",inOrchestratorPort=80):
    lResponse=DataSend(inKeyList,False,inOrchestratorHost,inOrchestratorPort)
    return lResponse