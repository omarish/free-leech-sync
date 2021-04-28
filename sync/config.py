import requests
import os
from pathlib import Path

SEARCH_BASE_URL = "https://themixingbowl.org/rssddl.xml?search="

if os.environ["HTTP_USERNAME"] and os.environ["HTTP_PASSWORD"]:
    HTTP_AUTH = requests.auth.HTTPBasicAuth(
        os.environ["HTTP_USERNAME"], os.environ["HTTP_PASSWORD"]
    )
else:
    HTTP_AUTH = None

REMOTE_HOST = os.environ["REMOTE_HOST"]
REMOTE_WATCH_PATH = Path("/home/user/Watch")
LOCAL_DATA_DIR = Path(os.getcwd()) / "data"
