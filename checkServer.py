from requests import get
from utils import get_Api
from notifypy.notify import Notify

notification = Notify(
    default_notification_icon="Resources/icofi.ico",
    default_notification_application_name="Fashion Paradise",
    default_notification_title="Billing Management System"
)
def checkServer(ping = True) -> bool:
    notification.message = "Checking Server Connection"
    notification.send()
    api = get_Api()
    try:
        req = get(api + "/connected", timeout=60)
        if req.status_code == 200:
            print("CONNECTED")
            if ping:
                notification.message = "Server Connected"
                notification.send()
            return True
        else:
            print("NOT CONNECTED")
            if ping:
                notification.message = "Server Not Connected"
                notification.send()
            return False
    except Exception:
        print("NOT CONNECTED")
        if ping:
            notification.message = "Server Not Connected"
            notification.send()
        return False

checkServer()