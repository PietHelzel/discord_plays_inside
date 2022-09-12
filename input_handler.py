from enum import Enum, auto

import time
import threading
import keyboard

class InputKey(Enum):
    RIGHT = auto()
    LEFT  = auto()
    UP    = auto()
    DOWN  = auto()
    GRAB  = auto()
    ENTER = auto()

    def to_str(self) -> str:
        match self:
            case InputKey.RIGHT: return "right arrow"
            case InputKey.LEFT : return "left arrow"
            case InputKey.UP   : return "up arrow"
            case InputKey.DOWN : return "down arrow"
            case InputKey.GRAB : return "Ctrl"
            case InputKey.ENTER: return "enter"

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
        self.release(InputKey.RIGHT)
        self.release(InputKey.LEFT)
        self.release(InputKey.UP)
        self.release(InputKey.DOWN)
        self.release(InputKey.GRAB)
        self.release(InputKey.ENTER)

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