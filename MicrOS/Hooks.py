"""
Module is responsible for collect the additional
feature definition dedicated to micrOS framework.

Boot phase execution based on config
- initialize / preload modules to memory

Profiling info
- free memory monitoring between seperated phases
- memory block usage

Designed by Marcell Ban aka BxNxM
"""

#################################################################
#                           IMPORTS                             #
#################################################################
from ConfigHandler import cfgget, console_write
from InterpreterCore import execute_LM_function_Core
try:
    from micropython import mem_info
except Exception:
    mem_info = None
try:
    from machine import freq
except Exception:
    freq = None

#################################################################
#                          FUNCTIONS                            #
#################################################################


def bootup_hook():
    """
    Executes when system boots up.
    """
    console_write("[BOOT HOOKS] EXECUTION...")
    if cfgget('boothook') is not None and cfgget('boothook').lower() != 'n/a':
        for shell_cmd in (cmd.strip() for cmd in tuple(cfgget('boothook').split(';')) if len(cmd.split()) > 1):
            console_write("|-[BOOT HOOKS] SHELL EXEC: {}".format(shell_cmd))
            try:
                state = execute_LM_function_Core(shell_cmd.split())
                console_write("|-[BOOT HOOKS] state: {}".format(state))
            except Exception as e:
                console_write("|--[BOOT HOOKS] error: {}".format(e))

    if cfgget('boostmd') is True:
        console_write("[BOOT HOOKS] Set up CPU 16MHz - boostmd: {}".format(cfgget('boostmd')))
        if freq is not None: freq(160000000)
    else:
        console_write("[BOOT HOOKS] Set up CPU 8MHz - boostmd: {}".format(cfgget('boostmd')))
        if freq is not None: freq(80000000)


def profiling_info(label=""):
    """
    Runtime memory measurements
    """
    if cfgget('dbg'):
        console_write("{} [PROFILING INFO] - {} {}".format('~'*5, label, '~'*5))
        try:
            if mem_info is not None: mem_info()
        except Exception as e:
            console_write("MEM INFO QUERY ERROR: {}".format(e))
        console_write("~"*30)
    else:
        console_write("[PROFILING INFO] SKIP dbg:{}".format(cfgget('dbg')))
