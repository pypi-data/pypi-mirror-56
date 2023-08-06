# -*- coding: utf-8 -*-

"""Interface for jtac"""

import sys
import click
import jtac.logic as arma
import wmi
import time

@click.group()
def main(args=None):
    pass

@main.command()
def debug():
    arma.debug()

@main.command('generate')
@click.option(
    '-P', '--process', default='arma3server_x64.exe', help='Arma3server executable name')
def generate_servers(process):
    """generates the servers.json file where I store your servers parameters"""
    arma.generate_servers(process)

@main.command('kill')
@click.argument('port')
def kill_server(port):
    """request our sniper (callsign SIERRA) to kill a server in particular"""
    arma.kill_server(port)

@main.command('start')
@click.argument('port')
@click.option(
    '-m', '--mission', help='select the mission that loads the server once started'
)
def start_server(port, mission):
    """starts a server with the parameters in servers.json that match given port"""
    arma.start_server(port)

@main.command('restart')
@click.argument('port')
def restart_server(port):
    """kills the server and revive it using chaman magic"""
    arma.kill_server(port)
    time.sleep(3)
    arma.start_server(port)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
