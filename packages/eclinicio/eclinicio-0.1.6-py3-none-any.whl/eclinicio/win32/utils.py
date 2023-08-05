from win32event import CreateMutex
from win32api import GetLastError
from winerror import ERROR_ALREADY_EXISTS


class SingleInstance:
    """ Limits application to single instance """

    def __init__(self):
        self.mutexname = "Eclinic_{D0E858DF-985E-4907-B7FB-8D732C3FC3B9}"
        self.mutex = CreateMutex(None, False, self.mutexname)
        self.lasterror = GetLastError()

    def already_running(self):
        return (self.lasterror == ERROR_ALREADY_EXISTS)


# getting idle duration on win32
from ctypes import Structure, windll, c_uint, c_int, byref, sizeof


class LastCPUInfo(Structure):
    _fields_ = [('cbSize', c_uint), ('dwTime', c_int)]


def get_idle_duration():
    lastInputInfo = LastCPUInfo()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
        millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
        return int(millis / 1000.0)
    else:
        return 0
