#coding: utf-8


class Logger(object):
    def __init__(self, level):
        self._levels = {
            0: "No debug",
            1: "Error only",
            2: "Full debug"
        }
        self._level = level

    def Log(self, debug_type, method_name, message):
        if self._level == 0:
            return
        if self._level == 1 and debug_type != "ERROR":
            return
        string = f"[{debug_type}][{method_name}] {message}"
        print(string)
