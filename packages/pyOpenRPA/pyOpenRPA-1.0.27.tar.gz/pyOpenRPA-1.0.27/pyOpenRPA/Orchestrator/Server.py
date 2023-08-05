from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from threading import Thread
from . import Processor
import importlib
import pdb
import base64
import uuid
import datetime
import os #for path operations
from http import cookies
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)
global mGlobalDict


def SaveScreenshot(inFilePath):
    # grab fullscreen
    # Save the entire virtual screen as a PNG
    lScreenshot = getScreenAsImage()
    lScreenshot.save('screenshot.png', format='png')
    #lScreenshot = ScreenshotSecondScreen.grab_screen()
    # save image file
    #lScreenshot.save('screenshot.png')

#inGlobalDict
# "JSONConfigurationDict":<JSON>
class RobotDaemonServer(Thread):
    def __init__(self,name,inGlobalDict):
        Thread.__init__(self)
        self.name = name
    def run(self):
        inServerAddress="";
        inPort = mGlobalDict["Server"]["ListenPort"];
        print('starting server..., port:'+str(inPort)+" inAddress:"+inServerAddress)
        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        server_address = (inServerAddress, inPort)
        httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
        print('running server...')
        httpd.serve_forever() 

#Authenticate function ()
# return dict
# {
#   "Domain": "", #Empty if Auth is not success
#   "User": "" #Empty if Auth is not success
# }
def AuthenticateVerify(inRequest):
    lResult={"Domain": "", "User": ""}
    ######################################
    #Way 1 - try to find AuthToken
    lCookies = cookies.SimpleCookie(inRequest.headers.get("Cookie", ""))
    #pdb.set_trace()
    if "AuthToken" in lCookies:
        lCookieAuthToken = lCookies.get("AuthToken", "").value
        if lCookieAuthToken:
            #Find AuthToken in GlobalDict
            if lCookieAuthToken in mGlobalDict.get("Server", {}).get("AccessUsers", {}).get("AuthTokensDict", {}):
                #Auth Token Has Been Founded
                lResult["Domain"] = mGlobalDict["Server"]["AccessUsers"]["AuthTokensDict"][lCookieAuthToken]["Domain"]
                lResult["User"] = mGlobalDict["Server"]["AccessUsers"]["AuthTokensDict"][lCookieAuthToken]["User"]
                #Exit earlier
                return lResult
    ######################################
    #Way 2 - try to logon
    lHeaderAuthorization = inRequest.headers.get("Authorization", "").split(" ")
    if len(lHeaderAuthorization) == 2:
        llHeaderAuthorizationDecodedUserPasswordList = base64.b64decode(lHeaderAuthorization[1]).decode("utf-8").split(
            ":")
        lUser = llHeaderAuthorizationDecodedUserPasswordList[0]
        lPassword = llHeaderAuthorizationDecodedUserPasswordList[1]
        lDomain = None
        if "\\" in lUser:
            lDomain = lUser.split("\\")[0]
            lUser = lUser.split("\\")[1]
        #Try to logon - use processor
        lLogonResult = Processor.Activity(
            {
                "Type": "WindowsLogon",
                "Domain": lDomain,
                "User": lUser,
                "Password": lPassword
            }
        )
        #Check result
        if lLogonResult["Result"]:
            lResult["Domain"] = lLogonResult["Domain"]
            lResult["User"] = lLogonResult["User"]
            #Create token
            lAuthToken=str(uuid.uuid1())
            mGlobalDict["Server"]["AccessUsers"]["AuthTokensDict"][lAuthToken] = {}
            mGlobalDict["Server"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["Domain"] = lResult["Domain"]
            mGlobalDict["Server"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["User"] = lResult["User"]
            mGlobalDict["Server"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["TokenDatetime"] = datetime.datetime.now()
            #Set-cookie
            inRequest.OpenRPA={}
            inRequest.OpenRPA["AuthToken"] = lAuthToken
            #inRequest.OpenRPAResponse["Set-Cookie"]=[]lResult["Set-Cookie"] = lAuthToken
            #pdb.set_trace()
            #inRequest.send_header("Set-Cookie:", f"AuthToken={lAuthToken}")
    ######################################
    return lResult
def AuthenticateBlock(inRequest):
    # Send response status code
    inRequest.send_response(401)
    # Send headers
    inRequest.send_header('Content-type', 'text/html')
    inRequest.send_header('WWW-Authenticate', 'Basic')  # Always ask login pass
    inRequest.end_headers()
    # Write content as utf-8 data
    inRequest.wfile.write(bytes("", "utf8"))
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    #ResponseContentTypeFile
    def SendResponseContentTypeFile(self, inContentType, inFilePath):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', inContentType)
        #Check if var exist
        if hasattr(self, "OpenRPA"):
            self.send_header("Set-Cookie", f"AuthToken={self.OpenRPA['AuthToken']}")
        self.end_headers()
        lFileObject = open(inFilePath, "rb") 
        # Write content as utf-8 data
        self.wfile.write(lFileObject.read())
        #Закрыть файловый объект
        lFileObject.close()        
    # GET
    def do_GET(self):
        #####################################
        #Do authentication
        #Check if authentication is turned on
        #####################################
        lFlagAccessUserBlock=False
        lAuthenticateDict = {"Domain": "", "User": ""}
        if mGlobalDict.get("Server", {}).get("AccessUsers", {}).get("FlagCredentialsAsk", False):
            lAuthenticateDict = AuthenticateVerify(self)
            if not lAuthenticateDict["User"]:
                lFlagAccessUserBlock=True
        if lFlagAccessUserBlock:
            AuthenticateBlock(self)
        #####################################
        else:
            lOrchestratorFolder = "\\".join(__file__.split("\\")[:-1])
            #Мост между файлом и http запросом (новый формат)
            if self.path == "/":
                self.SendResponseContentTypeFile('text/html', os.path.join(lOrchestratorFolder, "Web\\Index.xhtml"))
            #Мост между файлом и http запросом (новый формат)
            if self.path == '/3rdParty/Semantic-UI-CSS-master/semantic.min.css':
                self.SendResponseContentTypeFile('text/css', os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.css"))
            #Мост между файлом и http запросом (новый формат)
            if self.path == '/3rdParty/Semantic-UI-CSS-master/semantic.min.js':
                self.SendResponseContentTypeFile('application/javascript', os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.js"))
            #Мост между файлом и http запросом (новый формат)
            if self.path == '/3rdParty/jQuery/jquery-3.1.1.min.js':
                self.SendResponseContentTypeFile('application/javascript', os.path.join(lOrchestratorFolder,"..\\Resources\\Web\\jQuery\\jquery-3.1.1.min.js"))
            #Мост между файлом и http запросом (новый формат)
            if self.path == '/3rdParty/Google/LatoItalic.css':
                self.SendResponseContentTypeFile('font/css', os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Google\\LatoItalic.css"))
            #Мост между файлом и http запросом (новый формат)
            if self.path == '/3rdParty/Semantic-UI-CSS-master/themes/default/assets/fonts/icons.woff2':
                self.SendResponseContentTypeFile('font/woff2', os.path.join(lOrchestratorFolder,"..\\Resources\\Web\\Semantic-UI-CSS-master\\themes\\default\\assets\\fonts\\icons.woff2"))
            #Мост между файлом и http запросом (новый формат)
            if self.path == '/favicon.ico':
                self.SendResponseContentTypeFile('image/x-icon', os.path.join(lOrchestratorFolder, "Web\\favicon.ico"))
            #Мост между файлом и http запросом (новый формат)
            if self.path == '/3rdParty/Handlebars/handlebars-v4.1.2.js':
                self.SendResponseContentTypeFile('application/javascript', os.path.join(lOrchestratorFolder,"..\\Resources\\Web\\Handlebars\\handlebars-v4.1.2.js"))
            #Получить скриншот
            if self.path.split("?")[0] == '/GetScreenshot':
                #Сохранить файл на диск
                SaveScreenshot("Screenshot.png")
                self.SendResponseContentTypeFile('image/png',"Screenshot.png")
            #Monitor
            if self.path == '/Monitor/JSONDaemonListGet':
                # Send response status code
                self.send_response(200)
                # Send headers
                self.send_header('Content-type','application/json')
                self.end_headers()
                # Send message back to client
                message = json.dumps(mGlobalDict)
                # Write content as utf-8 data
                self.wfile.write(bytes(message, "utf8"))
            if self.path == '/Monitor/ControlPanelDictGet':
                # Send response status code
                self.send_response(200)
                # Send headers
                self.send_header('Content-type','application/json')
                self.end_headers()
                #Create result JSON
                lResultJSON={"RenderRobotList":[]}
                lRenderFunctionsRobotList=mGlobalDict["ControlPanelDict"]["RobotList"]
                for lItem in lRenderFunctionsRobotList:
                    #Выполнить вызов и записать результат
                    lItemResultDict=lItem["RenderFunction"](mGlobalDict)
                    #RunFunction
                    lResultJSON["RenderRobotList"].append(lItemResultDict)
                # Send message back to client
                message = json.dumps(lResultJSON)
                # Write content as utf-8 data
                self.wfile.write(bytes(message, "utf8"))
            #Filemanager function
            if self.path.lower().startswith('/filemanager/'):
                lFileURL=self.path[13:]
                # check if file in FileURL - File Path Mapping Dict
                if lFileURL.lower() in mGlobalDict["FileManager"]["FileURLFilePathDict"]:
                    self.SendResponseContentTypeFile('application/octet-stream',mGlobalDict["FileManager"]["FileURLFilePathDict"][lFileURL])
            # Auth function
    # POST
    def do_POST(self):
        #####################################
        #Do authentication
        #Check if authentication is turned on
        #####################################
        lFlagAccessUserBlock=False
        lAuthenticateDict = {"Domain": "", "User": ""}
        if mGlobalDict.get("Server", {}).get("AccessUsers", {}).get("FlagCredentialsAsk", False):
            lAuthenticateDict = AuthenticateVerify(self)
            if not lAuthenticateDict["User"]:
                lFlagAccessUserBlock=True
        if lFlagAccessUserBlock:
            AuthenticateBlock(self)
        #####################################
        else:
            #Централизованная функция получения запросов/отправки
            if self.path == '/Utils/Processor':
                #ReadRequest
                lInputObject={}
                if self.headers.get('Content-Length') is not None:
                    lInputByteArrayLength = int(self.headers.get('Content-Length'))
                    lInputByteArray=self.rfile.read(lInputByteArrayLength)
                    #Превращение массива байт в объект
                    lInputObject=json.loads(lInputByteArray.decode('utf8'))
                # Send response status code
                self.send_response(200)
                # Send headers
                self.send_header('Content-type','application/json')
                self.end_headers()
                # Send message back to client
                message = json.dumps(Processor.ActivityListOrDict(lInputObject))
                # Write content as utf-8 data
                self.wfile.write(bytes(message, "utf8"))
            return