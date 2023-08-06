from pyOpenRPA.Robot import UIDesktop
from . import Connector
import pdb
#Check for session is closed. Reopen if detected. Always keep session is active
def Monitor(inGlobalDict, inListUpdateTimeout):
    while True:
        # UIOSelector list init
        lUIOSelectorList = []
        for lItem in inGlobalDict["RDPList"]:
            lUIOSelectorList.append([{"title_re": f"{lItem['SessionHex']} — .*", "backend": "win32"}])
        #Run wait command
        lRDPDissappearList = UIDesktop.UIOSelectorsSecs_WaitDisappear_List(lUIOSelectorList, inListUpdateTimeout)
        for lItem in lRDPDissappearList:
            #pdb.set_trace()
            #Session start
            Connector.Session(inGlobalDict["RDPList"][lItem])
    return None