from pyOpenRPA.Robot import UIDesktop
from . import Connector
import os
import pdb
#Check for session is closed. Reopen if detected. Always keep session is active
def Monitor(inGlobalDict, inListUpdateTimeout):
    lFlagWhile = True
    while lFlagWhile:
        # UIOSelector list init
        lUIOSelectorList = []
        for lItem in inGlobalDict["RDPList"]:
            lUIOSelectorList.append([{"title_re": f"{lItem['SessionHex']} — .*", "backend": "win32"}])
        #Run wait command
        lRDPDissappearList = UIDesktop.UIOSelectorsSecs_WaitDisappear_List(lUIOSelectorList, inListUpdateTimeout)
        #Analyze if flag safeturn off is activated
        if inGlobalDict.get("OrchestratorToRobotResetStorage",{}).get("SafeTurnOff",False):
            lFlagWhile=False
            #Set status disconnected for all RDP List
            for lItem in inGlobalDict["RDPList"]:
                lItem["FlagSessionIsActive"]=False
            #Kill all RDP sessions
            os.system('taskkill /F /im mstsc.exe')
            #Return from function
            return
        for lItem in lRDPDissappearList:
            inGlobalDict["RDPList"][lItem]["FlagSessionIsActive"] = False # Set flag that session is disconnected
            #pdb.set_trace()
            #Session start
            try:
                Connector.Session(inGlobalDict["RDPList"][lItem])
            except Exception:
                pass
    return None
#TODO Def garbage window cleaner (if connection was lost)