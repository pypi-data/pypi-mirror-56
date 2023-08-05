#Robot RDPActive settings
def Settings():
    mDict = {
        "RDPList":
        [
            {
                "Host": "77.77.22.22",  # Host address
                "Port": "7777",  # RDP Port
                "Login": "test",  # Login
                "Password": "test",  # Password
                "Screen": {
                    "Width": 1680, #Width of the remote desktop in pixels
                    "Height": 1050, #Height of the remote desktop in pixels
                    # "640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen
                    "FlagUseAllMonitors": False,  # True or False
                    "DepthBit": "32"  # "32" or "24" or "16" or "15"
                },
                "SessionHex":"" # Hex is created when robot runs
            }
        ]
    }
    return mDict