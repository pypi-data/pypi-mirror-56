import threading
from typing import Optional

from api.handler.script.ScriptPythonTaskHandler import ScriptPythonTaskHandler

holder = threading.local()


def cacheHandler() -> Optional[ScriptPythonTaskHandler]:
    try:
        return holder.key
    except:
        return None
