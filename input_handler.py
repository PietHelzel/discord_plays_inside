from enum import Enum, auto

import time
import threading
import keyboard

class InputKey(Enum):
    W     = auto()
    A     = auto()
    S     = auto()
    D     = auto()
    E     = auto()
    Q     = auto()
    SPACE = auto()
    CTRL  = auto()
    TAB   = auto()
    SHIFT = auto()
    ONE   = auto()
    TWO   = auto()
    THREE = auto()
    

    def to_str(self) -> str:
        match self:
            case InputKey.W : return "w"
            case InputKey.A : return "a"
            case InputKey.S : return "s"
            case InputKey.D : return "d"

            case InputKey.SPACE : return "space bar"
            case InputKey.SHIFT : return "shift"
            case InputKey.CTRL  : return "ctrl"

            case InputKey.E     : return "e"
            case InputKey.Q     : return "q"
            case InputKey.TAB   : return "tab"
            case InputKey.ONE   : return "1"
            case InputKey.TWO   : return "2"
            case InputKey.THREE : return "3"

class EventKind(Enum):
    PRESS   = auto()
    RELEASE = auto()

class Event:

    def __init__(self, time: float, key: InputKey, event_kind: EventKind):
        self.time = time
        self.key = key
        self.event_kind = event_kind

    def __str__(self) -> str:
        return "Time: {0} | Key: {1}, EventKind: {2}".format(self.time, self.key, self.event_kind)


class InputHandler:

    def __init__(self):
        self.events = []

    def register_event(self, time_offset: float, key: InputKey, event_kind: EventKind):
        new_time = time.time() + time_offset
        event = Event(new_time, key, event_kind)
        self.events.append(event)

    def register_keypress(self, start_offset: float, duration: float, key: InputKey):
        self.register_event(start_offset, key, EventKind.PRESS)
        self.register_event(start_offset + duration, key, EventKind.RELEASE)

    def stop_all(self):
        self.events.clear()
        self.release(InputKey.W)
        self.release(InputKey.A)
        self.release(InputKey.S)
        self.release(InputKey.D)

    def run(self):
        threading.Thread(target=self.__run_threaded).start()

    def __run_threaded(self):
        while True:
            current_time = time.time()

            for index, event in enumerate(self.events):
                if event.time < current_time:
                    print(str(event))
                    if event.event_kind is EventKind.PRESS:
                        self.press(event.key)
                    elif event.event_kind is EventKind.RELEASE:
                        self.release(event.key)

                    self.events.pop(index)

            time.sleep(0.01)

    def press(self, key: InputKey):
        keyboard.press(key.to_str())
    
    def release(self, key: InputKey):
        keyboard.release(key.to_str())