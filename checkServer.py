from requests import get
from utils import get_Api
from notifypy.notify import Notify
from os import path
pathJoiner = path.join

notification = Notify(
    default_notification_icon=pathJoiner("Resources", "icofi.ico"),
    default_notification_application_name="Fashion Paradise",
    default_notification_title="Billing Management System"
)
def checkServer(ping = True, verbose = True) -> bool:
    if ping:
        notification.message = "Checking Server Connection"
        notification.send()
    api = get_Api()
    try:
        req = get(api + "/connected", timeout=60)
        if req.status_code == 200:
            if verbose: print("CONNECTED")
            if ping:
                notification.message = "Server Connected"
                notification.send()
            return True
        else:
            if verbose: print("NOT CONNECTED")
            if ping:
                notification.message = "Server Not Connected"
                notification.send()
            return False
    except Exception:
        if verbose: print("NOT CONNECTED")
        if ping:
            notification.message = "Server Not Connected"
            notification.send()
        return False
if __name__ == "__main__":
    checkServer()