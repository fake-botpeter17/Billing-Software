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

if __name__ == "__main__":
    checkServer()