
import os
from enum import Enum

class Mode(Enum):
    ONLINE = "online"
    OFFLINE = "offline"

class SystemMode:
    _instance = None
    _current_mode = Mode.ONLINE

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemMode, cls).__new__(cls)
            # Initialize from ENV or Default
            env_mode = os.getenv("ABRISK_MODE", "online").lower()
            cls._instance._current_mode = Mode.ONLINE if env_mode == "online" else Mode.OFFLINE
        return cls._instance

    @property
    def mode(self) -> str:
        return self._current_mode.value

    def set_mode(self, mode: str):
        if mode.lower() == "online":
            self._current_mode = Mode.ONLINE
        else:
            self._current_mode = Mode.OFFLINE

    @property
    def is_online(self) -> bool:
        return self._current_mode == Mode.ONLINE

    @property
    def is_demo(self) -> bool:
        return os.getenv("ABRISK_DEMO_MODE", "false").lower() == "true"

system_mode = SystemMode()
