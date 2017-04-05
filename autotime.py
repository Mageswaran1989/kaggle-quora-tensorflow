"""Ipython Cell Magic - Addons Functions.

Features

    * prints time for each cell execution
    * For cell took more than 100 Seconds
        * show start_time & end_time in human readable format
        * gives a beep sound
            * if you are using ITERM - you might see a notication also.

Usage: Execute following in you Ipython Notebook

    * To load `%load autotime`
    * To unload `%unload autotime`
    * To reload `%reload autotime`
"""
from __future__ import print_function

import time
from os import system
from IPython.core.magics.execution import _format_time as format_delta


class LineWatcher(object):
    """Class that implements a basic timer.

    Notes
    -----
    * Register the `start` and `stop` methods with the IPython events API.
    """

    def __init__(self):
        """Initialise params."""
        self.start_time = 0.0

    def start(self):
        """Set start_time."""
        self.start_time = time.time()

    def stop(self):
        """Show results."""
        if self.start_time:
            diff = time.time() - self.start_time
            epoch_start_time = pretty_date_time(self.start_time)
            epoch_end_time = pretty_date_time(time.time())
            assert diff > 0
            if diff > 100:
                print('duration:', epoch_start_time, "\t<->\t", epoch_end_time)
                # print('\a')
                system("tput bel")
            print('time: %s' % format_delta(diff))


def pretty_date_time(epoch_time):
    """Return a human readable datetime."""
    return (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time)))


timer = LineWatcher()


def load_ipython_extension(ip):
    """Register the cell execution start."""
    ip.events.register('pre_run_cell', timer.start)
    ip.events.register('post_run_cell', timer.stop)


def unload_ipython_extension(ip):
    """Register the cell execution end."""
    ip.events.unregister('pre_run_cell', timer.start)
    ip.events.unregister('post_run_cell', timer.stop)
