# !/usr/bin/env python3
# -*- coding: utf-8 -*-

#   ___      _  _     _               
#  | _ \_  _| || |___| |_ __  ___ _ _ 
#  |  _/ || | __ / -_) | '_ \/ -_) '_|
#  |_|  \_, |_||_\___|_| .__/\___|_|  
#       |__/           |_|            

# Pyhelper - Packages that provide more helper tools for Python
# Copyright (C) 2023-2024   Gao Yuhan(高宇涵)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library Public
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# DON'T EVEN HAVE A PERMIT TOO!
#
# Gao Yuhan(高宇涵)
# 2602422835@qq.com
# nanocode38

"""
A library that provides game help without dependencies
Copyright (C)
"""
import time
import tkinter as tk

from pyhelper.gamehelpers import pghelper
import pyhelper.gamehelpers.pghelper.widgets
from typing import *

__all__ = [
    'Timer',
    'CountUpTimer',
    'CountDownTimer',
    'game_help_window'
]


def game_help_window(help_text: str, title: str = 'Game Help'):
    """
    The function used to display help text for the game
    :param help_text: Help text to display
    :param title: popup title, Default: 'Game Help'
    """
    root = tk.Tk()
    root.title(title)
    root.resizable(True, True)
    root.wm_attributes("-topmost", 1)
    lable = tk.Label(root, text=help_text)
    lable.pack()

    root.update()

    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()


class Timer:
    """A class to manage a timer with the option to execute a command after the timer finishes.
    :param time_in_seconds: The time in seconds the timer should run for. default: -1, It's infinite
    :param command: The command to execute after the timer finishes. default: None

    Attributes:
        time_in_seconds (float): The time in seconds the timer should run for.
        is_running (bool)(read only): Whether the timer is running or not.
        start_time (float)(read only): The time in seconds the timer started.
    """

    def __init__(self, time_in_seconds: float = -1, command: Callable = None):
        self.time_in_seconds = time_in_seconds
        self._saved_time = 0.0
        self.__command = command
        self.__is_running = False
        self.__start_time = 0.0

    @property
    def start_time(self):
        return self.__start_time

    @property
    def is_running(self):
        return self.__is_running

    def start(self, new_time_in_seconds=-1) -> None:
        """Start the timer with the option to change the time in seconds."""

        if new_time_in_seconds != -1:
            self.time_in_seconds = new_time_in_seconds
        self.__is_running = True
        self.__start_time = time.time()

    def update(self) -> None:
        """Update the timer's saved time."""

        if not self.__is_running:
            return
        self._saved_time = time.time() - self.__start_time
        if self._saved_time < self.time_in_seconds or self.time_in_seconds < 0:
            return

        # timer has finished
        self.stop()

    def pause(self) -> None:
        """Pause the timer."""

        self.__is_running = False

    def go_on(self) -> None:
        """Resume the timer."""

        self.__is_running = True
        self.update()

    def get_time(self, number_of_reserved_bits=2) -> float:
        """Get the timer's saved time, updating it if the timer is running."""

        if self.__is_running:
            self._saved_time = round(time.time() - self.__start_time, number_of_reserved_bits)

        return self._saved_time

    def stop(self) -> None:
        """Stop the timer and execute the command if provided."""

        self.get_time()  # Remembers final self._saved_time
        self.__is_running = False
        if self.__command is not None:
            self.__command()
        return self.get_time()


class CountUpTimer:
    """
    A class to create a count-up timer that can be paused and resumed.
    This class is a subclass of the Timer class.

    :param start_time: The start time of the timer, in seconds, Default 0.0

    Attributes:
        is_running (read only): A boolean indicating whether the timer is running.
        saved_time (read only): The time the timer was paused at.
        is_pause: A boolean indicating whether the timer is paused.
    """

    def __init__(self, start_time: float = 0.0):
        self.__is_running = False
        self.__saved_time = 0.0
        self.__start_time = start_time + time.time()  # safeguard
        self.is_pause = False

    @property
    def is_running(self):
        """Return True if the timer is running, False otherwise."""
        return self.__is_running

    @property
    def start_time(self):
        """Return the start time of the timer."""
        return self.__start_time

    def start(self) -> None:
        """Start the timer."""
        if self.is_pause:
            self.__start_time = time.time()
            # get the cutter seconds and save the value
            self.__saved_time = 0.0
        self.__is_running = True
        self.is_pause = True

    def _get_time(self):
        """
        Return the current time of the timer.
        This is an internal private method. If you are reading this document, you are a bad client programmer!!
        """
        if not self.__is_running:
            return self.__saved_time

        self.__saved_time = time.time() - self.__start_time
        return self.__saved_time

    def get_time(self, mode='seconds') -> Union[str, float]:
        """
        Return the current time of the timer in the specified format.

        :param mode: The format of the time to be returned. If 'seconds', return the time in seconds. If 'HHMMSS',
            return the time as HH:MM:SS.

        :return str | float:
            If the mode is 'HHMMSS': str: The current time of the timer in the specified format.
            Else: float: The current time of the timer in seconds.
        """
        if mode != 'HHMMSS':
            return self._get_time()
        seconds = self._get_time()
        _min, sec = divmod(seconds, 60)
        hours, _min = divmod(int(_min), 60)
        strmin = str(_min)
        strhours = str(hours)
        strsec = str(sec)
        if _min < 10:
            strmin = '0' + strmin
        if hours < 10:
            strhours = '0' + strhours
        if sec < 10:
            strsec = '0' + strsec
        strsec = strsec[:6]
        return f'{strhours}:{strmin}:{strsec}'

    def stop(self) -> None:
        """Stop the timer."""
        self.get_time()  # remembers final self._saved_time
        self.__is_running = False


class CountDownTimer:
    """
    A class to create a count-up timer that can be paused and resumed.
    This class is a subclass of the Timer class.

    :param str_start_time: The start time of the timer, in 'HH:MM:SS'
    :param command: Automatically call at the end of the countdown
    """

    def __init__(self, str_start_time: str, command: Callable = None):
        list_time = str_start_time.split(':')
        hours = int(list_time[0])
        _min = int(list_time[1])
        sec = float(list_time[2])
        self.seconds = hours * 3600 + _min * 60 + sec
        if command is not None:
            self.timer = Timer(self.seconds, command)
        else:
            self.timer = Timer(self.seconds)

    def start(self) -> None:
        """Start the timer."""
        self.timer.start()

    def update(self) -> None:
        """Update the timer."""
        self.timer.update()

    def pause(self) -> None:
        """Pause the timer."""
        self.timer.pause()

    def go_on(self) -> None:
        """Resume the timer."""
        self.timer.go_on()
        self.update()

    def get_time(self, mode='seconds') -> Union[str, float]:
        """
        Return the current time of the timer in the specified format.

        :param mode: The format of the time to be returned. If 'seconds', return the time in seconds. If 'HHMMSS',
            return the time as HH:MM:SS.

        :return str | float:
            If the mode is 'HHMMSS': str: The current time of the timer in the specified format.
            Else: float: The current time of the timer in seconds.
        """
        saved_time = self.seconds - self.timer._saved_time
        if mode != 'HHMMSS':
            return saved_time
        _min, sec = divmod(saved_time, 60)
        hours, _min = divmod(int(_min), 60)
        strmin = str(_min)
        strhours = str(hours)
        strsec = str(sec)
        if _min < 10:
            strmin = '0' + strmin
        if hours < 10:
            strhours = '0' + strhours
        if sec < 10:
            strsec = '0' + strsec
        strsec = strsec[:6]
        return f'{strhours}:{strmin}:{strsec}'

    def stop(self) -> None:
        """Stop the Timer"""
        self.timer.stop()
