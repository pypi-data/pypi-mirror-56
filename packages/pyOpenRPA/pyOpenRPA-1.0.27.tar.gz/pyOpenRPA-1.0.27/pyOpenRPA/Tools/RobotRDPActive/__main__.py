#Import parent folder to import current / other packages
#########################################################
import sys
#lFolderPath = "\\".join(__file__.split("\\")[:-4])
lFolderPath = "/".join(__file__.split("/")[:-4])
sys.path.insert(0, lFolderPath)
#########################################################
from pyOpenRPA.Tools.RobotRDPActive import RDPConnector
mConfiguration={
    "Host": "77.77.22.22", #Host address
    "Port": "7777", #RDP Port
    "Login": "test", # Login
    "Password": "test", #Password
    "Screen": {
        "Resolution":"FullScreen", #"640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen
        "FlagUseAllMonitors": False, # True or False
        "DepthBit":"" #"32" or "24" or "16" or "15"
    }
}
RDPConnector.SessionConnect(mConfiguration)