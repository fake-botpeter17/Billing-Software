from threading import Thread, Event
from pickle import load
from requests import get
from os.path import join as pathJoiner
from logging import error
 
def run_check_server_periodically():
    def check_server_task():
        while True:
            try:
                checkServer(verbose=False)
            except Exception as e:
                error(f"Error during server check: {e}", exc_info=True)
            Event().wait(180)  # Wait for 3 minutes (180 seconds)

    thread = Thread(target=check_server_task, daemon=True)
    thread.start()

def checkServer(verbose = True) -> bool:
    api = get_Api()
    try:
        req = get(api + "/connected", timeout=60)
        if req.status_code == 200:
            if verbose: print("CONNECTED")
            return True
        else:
            if verbose: print("NOT CONNECTED")
            return False
    except Exception:
        if verbose: print("NOT CONNECTED")
        return False

def get_Api(testing: bool = False) -> str:
    """Returns the API URL for the server"""
    if testing:
        return "http://127.0.0.1:5000"

    with open(pathJoiner("Resources", "sak.dat"), "rb") as file:
        return load(file).decode("utf-32")