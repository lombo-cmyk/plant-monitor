import os
from datetime import datetime, timedelta

import psutil


def get_uptime() -> timedelta:
    p = psutil.Process(os.getpid())
    creation_time = datetime.fromtimestamp(p.create_time()).replace(microsecond=0)
    return datetime.now().replace(microsecond=0) - creation_time
