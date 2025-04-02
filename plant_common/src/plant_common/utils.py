import os
from datetime import datetime, timedelta

import psutil


def get_uptime() -> timedelta:
    p = psutil.Process(os.getpid())
    creation_time = datetime.fromtimestamp(p.create_time())
    return datetime.now() - creation_time
