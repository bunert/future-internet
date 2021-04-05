from enum import Enum


class CALLBACK_EVENT(Enum):
    INIT = 0
    DOWNLOAD_COMPLETED = 1
    TIMEOUT = 2
    REBUFFERING = 3
