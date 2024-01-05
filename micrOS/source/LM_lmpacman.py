from os import listdir, remove
from Common import socket_stream
from sys import modules


@socket_stream
def listmods(msgobj=None):
    """
    Load module package manager
    - list all load modules
    """
    # Dump available LMs
    msg_buf = []
    for k in (res.replace('LM_', '') for res in listdir() if res.startswith('LM_') or res.endswith('.html')):
        if msgobj is None:
            msg_buf.append('   {}'.format(k))
        else:
            msgobj('   {}'.format(k))
    return msg_buf if len(msg_buf) > 0 else ''


def dellm(lm=None):
    """
    Load module package manager
    - delete load module
    :param lm: Delete Load Module with full name: module.py or module.mpy
    """
    if lm is not None and lm.endswith('py'):
        # LM exception list - system and lmpacman cannot be deleted
        if 'lmpacman.' in lm or 'system.' in lm:
            return f'Load module {lm} is in use, skip delete.'
        try:
            remove(f'LM_{lm}')
            return f'Delete module: {lm}'
        except Exception as e:
            return f'Cannot delete: {lm}: {e}'
    return f'Invalid value: {lm}'


def delhtml(html=None):
    """
    Load module package manager
    - delete load module
    :param lm: Delete Load Module with full name: module.py or module.mpy
    """
    if html is not None and html.endswith('.html'):
        # LM exception list - system and lmpacman cannot be deleted
        if 'index.html' == html.strip():
            return f'Main page {html} is protected, skip delete.'
        try:
            remove(f'{html}')
            return f'Delete html: {html}'
        except Exception as e:
            return f'Cannot html: {html}: {e}'
    return f'Invalid value: {html}'


def del_duplicates():
    """
    Load module package manager (Not just load modules)
    - delete duplicated .mpy and .py resources, keep .mpy resource!
    """
    msg_buf = []
    py = list((res.split('.')[0] for res in listdir() if res.endswith('.py')))       # Normally smaller list
    mpy = (res.split('.')[0] for res in listdir() if res.endswith('.mpy'))
    for m in mpy:
        # Iterate over mpy resources
        state = True
        if m in py and m != 'main':
            to_delete = f'{m}.py'
            try:
                remove(to_delete)
            except:
                state = False
            msg_buf.append('   Delete {} {}'.format(to_delete, state))
    return '\n'.join(msg_buf) if len(msg_buf) > 0 else 'Nothing to delete.'


def module(unload=None):
    """
    List / unload loaded upython Load Modules
    :param unload: module name to unload
    :param unload: None - list active modules
    :return str: verdict
    """
    if unload is None:
        return list(modules.keys())
    if unload in modules.keys():
        del modules[unload]
        return "Module unload {} done.".format(unload)
    return "Module unload {} failed.".format(unload)


@socket_stream
def micros_checksum(msgobj=None):
    from hashlib import sha1
    from binascii import hexlify
    from os import listdir
    from Config import cfgget

    for f_name in (_pds for _pds in listdir() if _pds.endswith('py')):
        with open(f_name, 'rb') as f:
            cs = hexlify(sha1(f.read()).digest()).decode('utf-8')
        msgobj("{} {}".format(cs, f_name))
    # GC collect?
    return "micrOS version: {}".format(cfgget('version'))


def help():
    return 'listmods', 'dellm lm=<module>.py/.mpy', 'del_duplicates',\
           'module unload="LM_rgb/None"', 'delhtml html=<page>.html', 'micros_checksum'
