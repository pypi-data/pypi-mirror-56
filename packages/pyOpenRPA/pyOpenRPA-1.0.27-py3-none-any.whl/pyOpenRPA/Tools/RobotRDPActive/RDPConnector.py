#Import parent folder to import current / other packages
from pyOpenRPA.Robot import UIDesktop #Lib to access RDP window
import os #os for process run
import time
#Connect to RDP session
"""
{
    "Host": "", #Host address
    "Port": "", #RDP Port
    "Login": "", # Login
    "Password": "", #Password
    "Screen": {
        "Resolution":"FullScreen", #"640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen
        "FlagUseAllMonitors": False, # True or False
        "DepthBit":"" #"32" or "24" or "16" or "15"
    }
}
"""
def SessionConnect(inRDPSessionConfiguration):
    #Run mstsc
    from pywinauto.application import Application
    lRDPApplication = Application(backend="uia").start("mstsc.exe")
    lProcessId = lRDPApplication.process
    #Expand the parameter section
    UIDesktop.UIOSelector_Get_UIO(
        [
            {"process": lProcessId, "backend": "uia"},
            {"class_name": "ToolbarWindow32"},
            {"title": "Показать параметры ", "control_type": "Button"}]
    ).click()
    #Select flag ask login/pass
    UIDesktop.UIOSelector_Get_UIO(
        [
            {"process": lProcessId, "backend": "win32"},
            {"title":"Общие"},
            {"title":"Учетные данные"},
            {"title":"&Всегда запрашивать учетные данные", "class_name":"Button"}]
    ).check()
    #Set host:port
    lHostPort=inRDPSessionConfiguration['Host']
    if 'Port' in inRDPSessionConfiguration:
        lHostPort=f"{lHostPort}:{inRDPSessionConfiguration['Port']}"
    UIDesktop.UIOSelector_Get_UIO(
        [
            {"process": lProcessId, "backend": "uia"},
            {"title": "Компьютер:"},
            {"title": "Компьютер:", "control_type": "Edit"}]
    ).set_text(f"{lHostPort}")
    #Set user

