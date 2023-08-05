#!coding: cp936
import os
import win32ras

class AdslConnector(object):
    def __init__(self, name=None, username=None, password=None):
        self.name = name
        self.username = username
        self.password = password
        for entry in win32ras.EnumEntries():
            if entry.lower() == name :
                self.connectionName = entry
                break
        else :
            self.connectionName = win32ras.EnumEntries()[0]

    def connect(self):
        cmd_str = 'rasdial "%s" %s %s' % (self.connectionName, self.username, self.password)
        result = os.system(cmd_str)
        return result

    def disconnect(self):
        cmd_str = 'rasdial "%s" /disconnect' % self.connectionName
        result = os.system(cmd_str)
        return result

    def reconnect(self):
        self.disconnect()
        self.connect()