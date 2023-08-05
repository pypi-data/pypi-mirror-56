import pdb
import json
import subprocess
import zlib
import os
from . import ProcessCommunicator
import importlib
import traceback
import logging
import sys
import datetime
import struct
import shutil
#Создать файл логирования
# add filemode="w" to overwrite
if not os.path.exists("Reports"):
    os.makedirs("Reports")
logging.basicConfig(filename="Reports\ReportRobotRun_"+datetime.datetime.now().strftime("%Y_%m_%d")+".log", level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

####################################
#Info: Main module of the Robot app (OpenRPA - Robot)
####################################

#Usage:
#Here you can run some activity or list of activities

#After import this module you can use the folowing functions:
#ActivityRun(inActivitySpecificationDict): outActivityResultDict - function - run activity (function or procedure)
#ActivityRunJSON(inActivitySpecificationDictJSON): outActivityResultDictJSON
#ActivityListRun(inActivitySpecificationDictList): outActivityResultDictList - function - run list of activities (function or procedure)
#ActivityListRunJSON(inActivitySpecificationDictListJSON): outActivityResultDictListJSON

#Naming:
#Activity - some action/list of actions
#Module - Any *.py file, which consist of area specific functions
#Argument

#inActivitySpecificationDict:
#{
#   ModuleName: <"GUI"|..., str>,
#   ActivityName: <Function or procedure name in module, str>,
#   ArgumentList: [<Argument 1, any type>, ...] - optional,
#   ArgumentDict: {<Argument 1 name, str>:<Argument 1 value, any type>, ...} - optional
#}

#outActivityResultDict:
#{
#   ActivitySpecificationDict: {
#       ModuleName: <"GUI"|..., str>,
#       ActivityName: <Function or procedure name in module, str>,
#       ArgumentList: [<Argument 1, any type>, ...] - optional,
#       ArgumentDict: {<Argument 1 name, str>: <Argument 1 value, any type>, ...} - optional
#   },
#   ErrorFlag: <Boolean flag - Activity result has error (true) or not (false), boolean>,
#   ErrorMessage: <Error message, str> - required if ErrorFlag is true,
#   ErrorTraceback: <Error traceback log, str> - required if ErrorFlag is true,
#   Result: <Result, returned from the Activity, int, str, boolean, list, dict> - required if ErrorFlag is false
#}

####################
#Section: Module initialization
####################
#Start childprocess - GUI Module 32 bit
#pdb.set_trace()
if not os.path.isfile("..\\Resources\\WPy32-3720\\python-3.7.2\\OpenRPARobotGUIx32.exe"):
    shutil.copyfile('..\\Resources\\WPy32-3720\\python-3.7.2\\python.exe',"..\\Resources\\WPy32-3720\\python-3.7.2\\OpenRPARobotGUIx32.exe")
mProcessGUI_x32 = subprocess.Popen(['..\\Resources\\WPy32-3720\\python-3.7.2\\OpenRPARobotGUIx32.exe',"-m",'pyOpenRPA.Robot'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#Start childprocess - GUI Module 64 bit - uncomment after WPy64 installation
ProcessCommunicator.ProcessChildSendObject(mProcessGUI_x32,{"ModuleName":"UIDesktop","ActivityName":"Get_OSBitnessInt","ArgumentList":[],"ArgumentDict":{}})
lOSBitness = ProcessCommunicator.ProcessChildReadWaitObject(mProcessGUI_x32)["Result"]

lProcessBitnessStr = str(struct.calcsize("P") * 8)
#start 64 if system support 64
mProcessGUI_x64 = None
if lOSBitness == 64:
    if not os.path.isfile("..\\Resources\\WPy64-3720\\python-3.7.2.amd64\\OpenRPARobotGUIx64.exe"):
        shutil.copyfile('..\\Resources\\WPy64-3720\\python-3.7.2.amd64\\python.exe',"..\\Resources\\WPy64-3720\\python-3.7.2.amd64\\OpenRPARobotGUIx64.exe")
    mProcessGUI_x64 = subprocess.Popen(['..\\Resources\\WPy64-3720\\python-3.7.2.amd64\\OpenRPARobotGUIx64.exe',"-m",'pyOpenRPA.Robot'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

####################
#Section: Activity
####################
def ActivityRun(inActivitySpecificationDict):
    #Выполнить отправку в модуль UIDesktop, если ModuleName == "UIDesktop"
    #pdb.set_trace()
    if inActivitySpecificationDict["ModuleName"] == "UIDesktop":
        if "ArgumentList" not in inActivitySpecificationDict:
            inActivitySpecificationDict["ArgumentList"]=[]
        if "ArgumentDict" not in inActivitySpecificationDict:
            inActivitySpecificationDict["ArgumentDict"]={}
            
        #Если mProcessGUI_x64 не инициализирован
        lFlagRun64=True
        if mProcessGUI_x64 is None:
            lFlagRun64=False
        else:
            if inActivitySpecificationDict["ActivityName"]=="UIOSelectorsSecs_WaitAppear_List":
                #Функция ожидания появления элементов (тк элементы могут быть недоступны, неизвестно в каком фреймворке каждый из них может появиться)
                lFlagRun64=True
            elif inActivitySpecificationDict["ActivityName"].startswith("UIOSelector") or inActivitySpecificationDict["ActivityName"].startswith("PWASpecification"):
                if len(inActivitySpecificationDict["ArgumentList"])>0:
                    if len(inActivitySpecificationDict["ArgumentList"][0])>0:
                        #Определение разрядности (32 и 64) для тех функций, где это необходимо
                        ######################################################
                        #Выполнить проверку разрядности через UIOSelector_Get_BitnessInt
                        #Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
                        #pdb.set_trace()
                        #Внимание! Проверка разрядности специально делается на процессе 64 бита, тк процесс 32 бита зависает на 35 итерации проверки
                        ProcessCommunicator.ProcessChildSendObject(mProcessGUI_x64,{"ModuleName":"UIDesktop","ActivityName":"UIOSelector_Get_BitnessInt","ArgumentList":[inActivitySpecificationDict["ArgumentList"][0]],"ArgumentDict":inActivitySpecificationDict["ArgumentDict"]})
                        #Получить ответ от дочернего процесса
                        lResponseObject=ProcessCommunicator.ProcessChildReadWaitObject(mProcessGUI_x64)
                        #pdb.set_trace()
                        if lResponseObject["Result"]==32:
                            lFlagRun64=False
        #Запуск 64
        #pdb.set_trace()
        if lFlagRun64:
            #Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
            ProcessCommunicator.ProcessChildSendObject(mProcessGUI_x64,inActivitySpecificationDict)
            #Получить ответ от дочернего процесса
            lResponseObject=ProcessCommunicator.ProcessChildReadWaitObject(mProcessGUI_x64)
        else:
        #Запуск 32
            #Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
            ProcessCommunicator.ProcessChildSendObject(mProcessGUI_x32,inActivitySpecificationDict)
            #Получить ответ от дочернего процесса
            lResponseObject=ProcessCommunicator.ProcessChildReadWaitObject(mProcessGUI_x32)
        
    #Остальные модули подключать и выполнять здесь
    else:
        lArgumentList=[]
        if "ArgumentList" in inActivitySpecificationDict:
            lArgumentList=inActivitySpecificationDict["ArgumentList"]
        lArgumentDict={}
        if "ArgumentDict" in inActivitySpecificationDict:
            lArgumentDict=inActivitySpecificationDict["ArgumentDict"]
        #Подготовить результирующую структуру
        lResponseObject={"ActivitySpecificationDict":inActivitySpecificationDict,"ErrorFlag":False}
        try:
            #Подключить модуль для вызова
            lModule=importlib.import_module(inActivitySpecificationDict["ModuleName"])
            #Найти функцию
            lFunction=getattr(lModule,inActivitySpecificationDict["ActivityName"])
            #Выполнить вызов и записать результат
            lResponseObject["Result"]=lFunction(*lArgumentList,**lArgumentDict)
        except Exception as e:
            #Установить флаг ошибки и передать тело ошибки
            lResponseObject["ErrorFlag"]=True
            lResponseObject["ErrorMessage"]=str(e)
            lResponseObject["ErrorTraceback"]=traceback.format_exc()
    return lResponseObject
#########################################################
#Run list of activities
#########################################################
def ActivityListRun(inActivitySpecificationDictList):
    lResult=[]
    for lItem in inActivitySpecificationDictList:
        lResult.append(ActivityRun(lItem))
    return lResult