"""Dark Souls Auto Save, now in Python3!"""
from argparse import ArgumentParser
from pathlib import Path
from os import mkdir, scandir
import os.path as os_path
from re import match
from threading import Thread, Event
from time import sleep
from datetime import datetime
from shutil import copy2
from sys import exit as sys_exit

SLASH = "\\"
HOME = str(Path.home()) + SLASH
PATHS = [
    "Documents\\NBGI\\DarkSouls\\",
    "Documents\\NBGI\\Dark Souls Remastered\\",
    "AppData\\Roaming\\DarkSoulsII",
    "AppData\\Roaming\\DarkSoulsIII"]
FILENAMES = [
    "DRAKS0005.sl2",
    "DARKSII0000.sl2",
    "DS2SOFS0000.sl2",
    "DS30000.sl2"]


def check_paths(path, filename):
    """ checks files and paths and creates DSAS specific paths"""
    if os_path.exists(path):
        with scandir(path) as scaneddir:
            for directory in scaneddir:
                if match(r"\d+", directory.name):
                    sid_path = path + directory.name + SLASH
                    sid_dsas_path = sid_path + "DSAS" + SLASH
                    if os_path.exists(sid_path + filename):
                        if not os_path.exists(sid_dsas_path):
                            mkdir(sid_dsas_path)
                        return sid_dsas_path, sid_path, filename
        if os_path.exists(path + filename):
            dsas_path = path + "DSAS" + SLASH
            if not os_path.exists(dsas_path):
                mkdir(dsas_path)
            return dsas_path, path, filename
        raise FileNotFoundError(
            "Could not find %s in save path %s" %
            (filename, path))
    raise FileNotFoundError("Could not find save path %s" % path)


def backup_save(dsas_path, path, filename, timer, stop_event):
    """ thread-run func that backs up the save"""
    inttimer = 0
    while not stop_event.is_set():
        if inttimer < timer:
            inttimer += 1
            sleep(1)
        else:
            inttimer = 0
            save_time = datetime.strftime(datetime.now(), "_%m_%d_%Y-%I_%M_%p")
            newfile = filename.split(
                ".")[0] + save_time + "." + filename.split(".")[1]
            copy2(path + filename, dsas_path + newfile)
            print("Saved", newfile)


def __main__():
    """ how main can it get """
    parser = ArgumentParser(
        description="Dark Souls Auto Save for DS 1/2/3",
        prog="Dark Souls Auto Save")
    parser.add_argument(
        "-m",
        "--mode",
        help="Sets DSAS to handle game",
        type=int,
        dest="mode",
        default=1,
        choices=[
            1,
            2,
            3])
    parser.add_argument(
        "-r",
        "--remaster",
        help="Sets DSAS to handle remastered/reworked game versions",
        nargs="?",
        const=True,
        dest="remastered",
        default=False)
    parser.add_argument(
        "-t",
        "--timer",
        help="Sets timer in minutes",
        type=int,
        dest="timer",
        default=5)
    args = parser.parse_args()
    path = None
    filename = None
    dsas_path = None
    if args.mode == 1:
        if args.remastered:
            dsas_path, path, filename = check_paths(
                HOME + PATHS[1], FILENAMES[0])
        else:
            dsas_path, path, filename = check_paths(
                HOME + PATHS[0], FILENAMES[0])
    elif args.mode == 2:
        if args.remastered:
            dsas_path, path, filename = check_paths(
                HOME + PATHS[2], FILENAMES[2])
        else:
            dsas_path, path, filename = check_paths(
                HOME + PATHS[2], FILENAMES[1])
    if args.mode == 3:
        dsas_path, path, filename = check_paths(HOME + PATHS[3], FILENAMES[3])
    stop_event = Event()
    thread = Thread(
        target=backup_save,
        args=(
            dsas_path,
            path,
            filename,
            args.timer * 60,
            stop_event))
    thread.start()
    input("Press Enter to stop at any given time!\n")
    stop_event.set()
    print("Exiting...")
    thread.join(timeout=5)
    print("Hope you didn't get $R3kt?\nCy@ Nub")
    sys_exit(0)


if __name__ == "__main__":
    __main__()
