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


def get_cpus() -> List:
    """
    Get the current usage stat of all processors.

    Args:
        None

    Returns:
        List: Current usage of each processor by index
    """

    return psutil.cpu_percent(interval=1, percpu=True)


def get_memory() -> float:

    return psutil.virtual_memory().percent


def get_net_io(all_if: list) -> Dict:

    net_io = {}

    all_if_info = psutil.net_io_counters(pernic=True)

    for net_if in all_if:
        net_io.update({
            net_if: {
                "bytes_sent": all_if_info[net_if].bytes_sent,
                "bytes_received": all_if_info[net_if].bytes_recv,
                "errin": all_if_info[net_if].errin,
                "errout": all_if_info[net_if].errout
            }
        })

    return net_io


def get_disks() -> List:

    part_info = []

    for part in psutil.disk_partitions():
        disk_usage = psutil.disk_usage(part.mountpoint)
        part_info.append({
            part.mountpoint: {
                "device": part.device,
                "fstype": part.fstype,
                "total_size": convert_size(disk_usage.total),
                "percent": disk_usage.percent
            }
        })

    return part_info


def get_proc_info() -> Dict:

    proc_info = {}

    for process in subprocess.run(["ps", "aux"], capture_output=True,
                                  text=True).stdout.split('\n'):
        split_proc = process.split()

        proc_info.update({
            split_proc[1]: {
                "USER": split_proc[0],
                "CPU": split_proc[2],
                "MEM": split_proc[3],
                "START": split_proc[8],
                "TIME": split_proc[9],
                "COMMAND": ' '.join(split_proc[10:])
            }
        })
    
    return proc_info


def search_proc(search: str, sensitive: bool) -> List:

    if sensitive:
        return subprocess.run(["pgrep", search], capture_output=True,
                              text=True).stdout.split()
    else:
        return subprocess.run(["pgrep", "-i", search], capture_output=True,
                              text=True).stdout.split()


def search_lsof(pids: list) -> List:

    lsof = []

    for file in subprocess.run(["lsof", "-p", ','.join(pids)], capture_output=True,
                               text=True).stdout.split('\n')[1:]:
        try:
            # grab the file by matching the regex
            lsof.append(re.search(r'/\D.*', ' '.join(file.split()[5:])).group())
        except AttributeError:
            # If the regex did not match a valid path, just continue
            pass

    return lsof


class PIDStats():
    """
    Get the stats associated with a list of PIDs. This includes user, pid, cpu%,
    mem%, start_datetime, command, and associated open files.
    """
    pass


class ScreenWriter():
    """
    Write the user selected information onto the screen based on the interval
    given. For efficiency only the parts that are dynamic are re-fetched and
    rebuilt.
    """
    pass


"""
############################# MAIN #############################
"""


def main():
    """
    Run the program. Accepts no inputs.
    """
    # Build and store user arguments
    parser = user_input()
    input_args = parser.parse_args()

    # Configure the logging object
    # gd.set_logging(input_args)


# Only run if executing, not import
if __name__ == "__main__":
    main()
