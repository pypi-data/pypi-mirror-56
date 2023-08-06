#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module has all the logic and hard stuff of the app"""

# imports
import wmi
from appdirs import AppDirs
import json
import os
import signal
import re

# global variables
_SERVERS = {"servers": []}
_APPDIR = AppDirs('jtac', 'corp-0').user_data_dir
_APPSTORE = _APPDIR + '/servers.json'
_PROCNAME = "arma3server_x64.exe"

# definición funnciones


def read_json(file):
    with open(file, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)

        return json_data


def write_json(data, file):
    with open(file, 'w', encoding='UTF-8') as file:
        json_data = json.dumps(data, indent=4, sort_keys=True)
        file.write(json_data)


def read_APPSTORE():
    global _SERVERS

    # check if file or dir doesn't exists
    if not (os.path.isdir(_APPDIR)) or not (os.path.isfile(_APPSTORE)):
        if not os.path.isdir(_APPDIR):
            os.makedirs(_APPDIR)
        generate_servers(_PROCNAME)
    else:
        _SERVERS = read_json(_APPSTORE)

        return _SERVERS


def active_servers():
    c = wmi.WMI()
    active_servers = []

    for process in c.Win32_Process():
        if process.Name == _PROCNAME:
            port = re.search('-port=(\d*)', str(process.CommandLine)).group(1)
            active_servers.append([port, process.ProcessId])

    return active_servers


def generate_servers(_PROCNAME):
    global _SERVERS

    if not (os.path.isdir(_APPDIR)) or not (os.path.isfile(_APPSTORE)):
        if not os.path.isdir(_APPDIR):
            os.makedirs(_APPDIR)

    server_list = []
    c = wmi.WMI().Win32_process()
    for element in c:
        if element.Name == _PROCNAME:
            cl = element.CommandLine
            port = re.search('-port=(\d*)', str(element.CommandLine)).group(1)
            data = {
                port: {
                    "PID": element.ProcessId,
                    "PARAMS": element.CommandLine
                }
            }
            server_list = _SERVERS['servers']

            for element in server_list:
                if port in element.keys():
                    server_list.pop(element)

            server_list.append(data)

    _SERVERS['servers'] = server_list
    write_json(_SERVERS, _APPSTORE)

    if not _SERVERS['servers']:
        raise Exception(
            "ERROR: I couldn't find any servers running. Remember to run your servers before this command")

    write_json(_SERVERS, _APPSTORE)


def find_server(port):
    read_APPSTORE()

    server_list = _SERVERS['servers']
    for element in server_list:
        if port in element.keys():
            target_server = element[port]
            return target_server

    return False


def kill_server(port):
    target_server = find_server(port)
    if not target_server:
        raise Exception("I couldn't find any server configured with that port")

    PID = target_server['PID']

    try:
        os.kill(PID, signal.SIGTERM)
    except Exception as e:
        print("Can't kill server at " + port)
        print(str(e))
    else:
        print('Server at '+port+' is gone!')


def start_server(port):
    target_server = find_server(port)
    if not target_server:
        raise Exception("I couldn't find any server configured with that port")

    c = wmi.WMI()
    c.Win32_Process.Create(CommandLine=target_server['PARAMS'])
    active = active_servers()
    for element in active:
        if port in element:
            current_server = element
            break
    PID = current_server[1]
    update_server_info(port, key='PID', value=PID)
    print('Server started at ' + port + ' with PID: ' + str(PID))


def update_server_info(port, **kwargs):
    global _SERVERS
    server_list = _SERVERS['servers']

    key = kwargs['key']
    value = kwargs['value']

    target_server = find_server(port)
    target_server[key] = value

    write_json(_SERVERS, _APPSTORE)

def debug():
    c = wmi.WMI().Win32_process()
    for element in c:
        if "arma3server" in element.Name:
            print(element.Name + ' || '+ str(element.ProcessId) +' || ' + str(element.CommandLine))

def main():
    """Launcher."""
    # init the GUI or anything else
    pass


if __name__ == "__main__":
    main()
