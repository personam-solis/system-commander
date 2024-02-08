#!/usr/bin/env python3

import argparse
import psutil
from typing import List, Dict, AnyStr
import re
import subprocess


def user_input() -> argparse.ArgumentParser:
    """
    Get user input
    """
    parser = argparse.ArgumentParser(description="""
Show local system stats based on user inputs. This shows the current state along
with historical average. This can also be used to trace a process with all open
files and usage.

REQUIRES frequency of poll in seconds.

Defaults to base stats:
    - System Info
    - Network I/O
    - Local Storage Capacity
    """, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--poll', '-p', metavar='SECONDS', type=int)
    parser.add_argument('--network', '-n')

    return parser


def convert_size(bytes: int) -> AnyStr:
    if len(str(bytes)) <= 3:
        return 'UNK'
    elif len(str(bytes)) <= 6:
        return f'{round(bytes / 1024, 1)} KB'
    elif len(str(bytes)) <= 6:
        return f'{round(bytes / 1024 / 1024, 1)} MB'
    elif len(str(bytes)) <= 6:
        return f'{round(bytes / 1024 / 1024 / 1024, 1)} GB'
    elif len(str(bytes)) <= 6:
        return f'{round(bytes / 1024 / 1024 / 1024 / 1024, 1)} TB'
    elif len(str(bytes)) <= 6:
        return f'{round(bytes / 1024 / 1024 / 1024 / 1024 / 1024, 1)} PB'


def get_sysinfo() -> Dict:
    sysinfo = {
        "system_name": psutil.os.uname().nodename,
        "cpu_count": psutil.cpu_count(),
        "os_release": psutil.os.uname().release,
        "architecture": psutil.os.uname().machine,
        "total_memory": convert_size(psutil.virtual_memory().total),
        "interface": []
    }

    # get interfaces and info
    all_if_info = psutil.net_if_addrs()

    # Remove all interfaces that are not needed (Docker, Podman, Local)
    for interface in list(all_if_info.keys()):
        if re.search(r'[Dd]ocker|[Pp]odman|lo', interface):
            all_if_info.pop(interface)

    # Add interface info to dict
    for interface in list(all_if_info.keys()):
        sysinfo['interface'].append({
            interface: {
                "ip": all_if_info[interface][0].address,
                "mac": all_if_info[interface][-1].address
            }
        })

    return sysinfo

