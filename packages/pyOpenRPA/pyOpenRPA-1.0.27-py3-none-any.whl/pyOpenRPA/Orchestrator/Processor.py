import datetime
import http.client
import json
import pdb
import os
import sys
import subprocess
import copy
import importlib
#Input arg
#       [
#           {
#               "Type": <RemoteMachineProcessingRun>,
#               host: <localhost>,
#               port: <port>,
#               bodyObject: <object dict, int, str, list>
#           },
#           {
#               "Type": "CMDStart",
#				"Command": ""
#           },
#           {
#               "Type": "OrchestratorRestart"
#           },
#           {
#               "Type": "GlobalDictKeyListValueSet",
#               "KeyList": ["key1","key2",...],
#               "Value": <List, Dict, String, int>
#           },
#           {
#               "Type": "GlobalDictKeyListValueGet",
#               "KeyList": ["key1","key2",...]
#           },
#           {
#               "Type":"ProcessStart",
#               "Path":"",
#               "ArgList":[]
#               
#           },
#           {
#               "Type":"ProcessStop",
#               "Name":"",
#               "FlagForce":True,
#               "User":"" #Empty, user or %username%
#           },
#           {
#               "Type":"PythonStart",
#               "ModuleName":"",
#               "FunctionName":"",
#               "ArgList":[],
#               "ArgDict":{}
#           },
#           {
#               "Type":"WindowsLogon",
#               "Domain":"",
#               "User":"",
#               "Password":""
#               # Return "Result": True - user is logged on, False - user is not logged on
#           }
#       ]
##################################
#Output result
# <input arg> with attributes:
# "DateTimeUTCStringStart"
# "DateTimeUTCStringStop"
# "Result"
def Activity(inActivity):
    #Глобальная переменная - глобальный словарь унаследованный от Settings.py
    global mGlobalDict
    #Fill DateTimeUTCStringStart
    inActivity["DateTimeUTCStringStart"] = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%dT%H:%M:%S.%f")
    #Alias (compatibility)
    lItem = inActivity
    ###########################################################
    #Обработка запроса на отправку команды на удаленную машину
    ###########################################################
    if lItem["Type"]=="RemoteMachineProcessingRun":
        lHTTPConnection = http.client.HTTPConnection(lItem["host"], lItem["port"], timeout=5)
        try:
            lHTTPConnection.request("POST","/ProcessingRun",json.dumps(lItem["bodyObject"]))
        except Exception as e:
            #Объединение словарей
            lItem["Result"] = {"State":"disconnected","ExceptionString":str(e)}
        else:
            lHTTPResponse=lHTTPConnection.getresponse()
            lHTTPResponseByteArray=lHTTPResponse.read()
            lItem["Result"] = json.loads(lHTTPResponseByteArray.decode('utf8'))
    ###########################################################
    #Обработка команды CMDStart
    ###########################################################
    if lItem["Type"]=="CMDStart":
        lCMDCode="cmd /c "+lItem["Command"]
        subprocess.Popen(lCMDCode)
        lResultCMDRun=1#os.system(lCMDCode)
        lItem["Result"] = str(lResultCMDRun)
    ###########################################################
    #Обработка команды OrchestratorRestart
    ###########################################################
    if lItem["Type"]=="OrchestratorRestart":
        os.execl(sys.executable,os.path.abspath(__file__),*sys.argv)
        lItem["Result"] = True
        sys.exit(0)
    ###########################################################
    #Обработка команды GlobalDictKeyListValueSet
    ###########################################################
    if lItem["Type"]=="GlobalDictKeyListValueSet":
        for lItem2 in lItem["KeyList"][:-1]:
            #Check if key - value exists
            if lItem2 in mGlobalDict:
                pass
            else:
                mGlobalDict[lItem2]={}
            mGlobalDict=mGlobalDict[lItem2]
        #Set value
        mGlobalDict[lItem["KeyList"][-1]]=lItem["value"]
    ###########################################################
    #Обработка команды GlobalDictKeyListValueGet
    ###########################################################
    if lItem["Type"]=="GlobalDictKeyListValueGet":
        for lItem2 in lItem["KeyList"][:-1]:
            #Check if key - value exists
            if lItem2 in mGlobalDict:
                pass
            else:
                mGlobalDict[lItem2]={}
            mGlobalDict=mGlobalDict[lItem2]
        #Return value
        lItem["Result"]==mGlobalDict.get(lItem["KeyList"][-1],None)
    #Определить вид активности
    lActivityDateTime=inActivity["DateTimeUTCStringStart"]
    #####################################
    #ProcessStart
    #####################################
    if lItem["Type"]=="ProcessStart":
        #Вид активности - запуск процесса
        #Запись в массив отработанных активностей
        #Лог
        mGlobalDict["Processor"]["LogList"].append({"activityType":lItem["activityType"], "activityDateTime":str(lActivityDateTime), "processPath":lItem["processPath"], "activityStartDateTime":str(lCurrentDateTime)})
        #Запустить процесс
        lItemArgs=[lItem["processPath"]]
        lItemArgs.extend(lItem["processArgs"])
        subprocess.Popen(lItemArgs,shell=True)
    #################################
    #ProcessStop
    #################################
    if lItem["Type"]=="ProcessStop":
        #Вид активности - остановка процесса
        #часовой пояс пока не учитываем
        #Сформировать команду на завершение
        lActivityCloseCommand='taskkill /im '+lItem["processName"]
        #TODO Сделать безопасную обработку,если параметра нет в конфигурации
        if lItem.get('FlagForce',False):
            lActivityCloseCommand+=" /F"
        #Завершить процессы только текущего пользоваиеля
        if lItem.get('User',"")!="":
            lActivityCloseCommand+=f' /fi "username eq {lItem["User"]}"'
        #Лог
        mGlobalDict["Processor"]["LogList"].append({"activityType":lItem["activityType"], "activityDateTime":str(lActivityDateTime), "processPath":lItem["processName"], "activityStartDateTime":str(lCurrentDateTime)})
        #Завершить процесс
        os.system(lActivityCloseCommand)
    #################################
    #PythonStart
    #################################
    if lItem["Type"]=="PythonStart":
        try:
            #Подключить модуль для вызова
            lModule=importlib.import_module(lItem["ModuleName"])
            #Найти функцию
            lFunction=getattr(lModule,lItem["FunctionName"])
            lItem["Result"]=lFunction(*lItem.get("ArgList",[]),**lItem.get("ArgDict",{}))
        except Exception as e:
            logging.exception("Loop activity error: module/function not founded")
    #################################
    # Windows logon
    #################################
    if lItem["Type"] == "WindowsLogon":
        import win32security
        try:
            hUser = win32security.LogonUser(
                lItem["User"],
                lItem["Domain"],
                lItem["Password"],
                win32security.LOGON32_LOGON_NETWORK,
                win32security.LOGON32_PROVIDER_DEFAULT
            )
        except win32security.error:
            lItem["Result"] = False
        else:
            lItem["Result"] = True
    ###################################
    #Set datetime stop
    lItem["DateTimeUTCStringStop"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    ##################
    #Trace activity
    ##################
    if mGlobalDict["Processor"].get(f"LogType_{lItem['Type']}",True):
        #Add activity in TransactionList if it is applicable
        mGlobalDict["Processor"]["LogList"].append(copy.deepcopy(lItem))
    #Вернуть результат
    return lItem

def ActivityListOrDict(inActivityListOrDict):
    #Check arg type (list or dict)
    if type(inActivityListOrDict)==list:
        #List activity
        lResult=[]
        for lItem in inActivityListOrDict:
            lResult.append(Activity(lItem))
        return lResult
    if type(inActivityListOrDict)==dict:
        #Dict activity
        return Activity(inActivityListOrDict)