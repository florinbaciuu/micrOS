#!/usr/bin/env python3
import json
import os
import sys
import time
import socket
import ast
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(MYPATH))
import socketClient
sys.path.append(os.path.join(MYPATH, '../lib/'))
from TerminalColors import Colors
import requests

# FILL OUT
DEVICE = '__simulator__'


def base_cmd():
    return ['--dev', DEVICE]


def get_device():
    return DEVICE


def single_cmd_exec_check():
    info = "[ST] Run single command execution check [hello]"
    print(info)
    cmd_list = ['hello']
    output = execute(cmd_list)
    if output[0]:
        if output[1].startswith("hello:"):
            return True, info
    return False, info


def lm_cmd_exec_check():
    info = "[ST] Run Load Module command execution check [system heartbeat]"
    print(info)
    cmd_list = ['system heartbeat']
    output = execute(cmd_list)
    if output[0]:
        if output[1].strip() == '<3 heartbeat <3':
            return True, info
    return False, info


def micrOS_config_get():
    info = "[ST] Run micrOS config get [conf -> socport]"
    print(info)
    cmd_list = ['config <a> socport']
    output = execute(cmd_list)
    if output[0]:
        if output[1].strip() == '9008':
            return True, info
    return False, info


def micrOS_config_set():
    info = "[ST] Run micrOS config set [conf -> utc]"
    utc_bak = None
    print(info)

    # [1] Get actual utc value
    cmd_list = ['config <a> utc']
    output = execute(cmd_list)
    if output[0]:
        try:
            utc_bak = int(output[1].strip())
        except:
            return False, f"{info} + get utc error: {output[1]}"

    # [2] Set x+1 value as expected
    utc_expected = utc_bak+1
    cmd_list = ['config <a> utc {}'.format(utc_expected)]
    output = execute(cmd_list)
    if output[0]:
        if output[1].strip() != 'Saved':
            return False, f"{info} + utc overwrite issue: {output[1]}"

    # [3] Get modified utc value - veridy [2] step
    cmd_list = ['config <a> utc']
    output = execute(cmd_list)
    if output[0]:
        if int(output[1].strip()) != utc_expected:
            return False, f"{info} + utc modified value error: {output[1]} != {utc_expected}"

    # Restore original value
    cmd_list = ['config <a> utc {}'.format(utc_bak)]
    output = execute(cmd_list)
    if output[0]:
        if output[1].strip() != 'Saved':
            return False, f"{info} + utc overwrite issue: {output[1]}"

    # Final verdict
    return True, info


def micrOS_bgjob_one_shot_check():
    info = "[ST] Run micrOS BgJob check [system clock &]"
    print(info)

    # Initial task cleanup...
    execute(['task kill system.clock'])

    async_available_cmd_list = ['help']
    output = execute(async_available_cmd_list)
    if output[0]:
        if "[TASK]" not in output[1]:
            return False, f'[ASYNC] task function not available: {output[1]}'
    else:
        return False, f'[ASYNC] check: help cmd return error.'

    for _ in range(0, 2):
        cmd_list = ['system clock &']
        output = execute(cmd_list)
        time.sleep(1)
        if output[0]:
            if 'Start system.clock' not in output[1].strip():
                return False, f'{info} + not expected return: {output[1]}'
    return True, info


def micrOS_bgjob_loop_check():
    info = "[ST] Run micrOS Async Task check [system clock &&] + task kill"
    print(info)

    async_available_cmd_list = ['help']
    output = execute(async_available_cmd_list)
    if output[0]:
        if "[TASK]" not in output[1]:
            return False, f'[ASYNC] task function not available: {output[1]}'
    else:
        return False, f'[ASYNC] check: help cmd return error.'

    # Start background task loop
    cmd_list = ['system clock &&']
    output = execute(cmd_list)
    if output[0]:
        if 'Start system.clock' not in output[1].strip():
            return False, f'[Start Task error] {info} + not expected return: {output[1]}'

    # Attempt to overload background thread
    cmd_list = ['system clock &&']
    output = execute(cmd_list)
    if output[0]:
        if 'system.clock is Busy' not in output[1].strip():
            return False, f'[Overload task - run same] {info} + not expected return: {output[1]}'

    # Show task output by task tag
    cmd_list = ['task show system.clock']
    output = execute(cmd_list)
    if output[0]:
        if "No task found" in output[1].strip() or len(output[1].strip()) == 0:
            return False, f'[No task output] {info} + not expected return: {output[1]}'

    # Stop BgJob
    cmd_list = ['task kill system.clock']
    output = execute(cmd_list)
    if output[0]:
        if 'Kill:' in output[1].strip() or 'system.clock' in output[1].strip():
            return True, f'[Stop task] {info}'

    # Failed verdict
    return False, f'[Thread not stopped]{info} + not expected return: {output[1]}'


def micrOS_get_version():
    info = "[ST] Run micrOS get version [version]"
    print(info)
    cmd_list = ['version']
    output = execute(cmd_list)
    if output[0]:
        if '.' in output[1].strip() and '-' in output[1].strip():
            return True, f"{info} v:{output[1].strip()}"
    return False, f"{info} out: {output[1]}"


def json_format_check():
    info = "[ST] Run micrOS raw output check aka >json [system rssi >json]"
    print(info)
    cmd_list = ['system rssi >json']
    output = execute(cmd_list)
    if output[0] and output[1].startswith("{") and output[1].endswith("}"):
        return True, info + f" out: {output[1]}"
    return False, info + f" out: {output[1]}"


def negative_interface_check():
    info = "[ST] Run micrOS Negative API check [Invalid CMDs + conf]"
    print(info)

    cmd_list = ['Apple']
    output = execute(cmd_list)
    if output[0]:
        if 'SHELL: type help for single word commands' not in output[1].strip():
            return False, f'[Wrong single command] {info} + not expected return: {output[1]}'

    cmd_list = ['Apple test']
    output = execute(cmd_list)
    if output[0]:
        if 'no module named' not in output[1].strip().lower():
            return False, f'[Missing module] {info} + not expected return: {output[1]}'

    cmd_list = ['conf', 'gmttimaaaa']
    output = execute(cmd_list)
    if output[0]:
        if output[1].strip() != 'None':
            return False, f'[Config invalid key] {info} + not expected return: {output[1]}'

    cmd_list = ['conf', 'utc "type"']
    output = execute(cmd_list)
    if output[0]:
        if output[1].strip() != 'Failed to save':
            return False, f'[Config invalid key type] {info} + not expected return: {output[1]}'

    return True, info


def measure_package_response_time():
    info = "[ST] Measure response time [system heartbeat]x10"
    print(info)
    cmd_list = ['system heartbeat',
                'system heartbeat',
                'system heartbeat',
                'system heartbeat',
                'system heartbeat',
                'system heartbeat',
                'system heartbeat',
                'system heartbeat',
                'system heartbeat',
                'system heartbeat']
    # Start time
    start = time.time()
    # Command exec
    output = execute(cmd_list)
    # Stop time
    end = time.time() - start
    # Get average response time
    delta_cmd_rep_time = round(end/10, 4)
    # Create verdict
    print(output)
    if output[0] and "<3 heartbeat <3" in output[1]:
        return True, info + f' deltaT: {delta_cmd_rep_time} s'
    return False, info + f' {output[0]}:{output[1]} deltaT: {delta_cmd_rep_time} s'


def micros_alarm_check():
    info = "[ST] Test alarm state - system alarms should be null"
    print(info)
    cmd_list = ['system alarms']
    output = execute(cmd_list)
    alarm_cnt = 0
    if output[0]:
        try:
            alarm_cnt = output[1].split(':')[-1]
            alarm_cnt = int(alarm_cnt.strip())
        except Exception as e:
            alarm_cnt = 404
            print(e)
        # Clean alarms
        cmd_list = ['system alarms True']
        execute(cmd_list)
        # Evaluation
        if alarm_cnt > 0:
            return True, info + f" -1 !!!WARN!!! [{alarm_cnt}] out: {output[1]}"
    return True, info + f" [{alarm_cnt}] out: {output[1]}"


def oled_msg_end_result(result):
    cmd_list = ['lmpacman module >json']
    output = execute(cmd_list)
    if output[0] and 'LM_oled_ui' in output[1]:
        cmd_list = [f'oled_ui msgbox "{result} %"']
        print(execute(cmd_list))


def check_device_by_hostname(dev):
    devlocal = '{}.local'.format(dev)
    info_msg = '[ST] Check host {} and resolve IP'.format(devlocal)
    print(info_msg)
    try:
        ip = socket.gethostbyname(devlocal)
    except Exception as e:
        ip = None
        return False, '{}: {} error: {}'.format(info_msg, ip, e)
    if '.' in ip:
        return True, '{}: {}'.format(info_msg, ip)
    return False, '{}: {}'.format(info_msg, ip)


def check_robustness_exception():
    info_msg = '[ST] Check robustness - exception [robustness raise_error]'
    print(info_msg)
    cmd_list = ['robustness raise_error']
    output = execute(cmd_list)
    if output[0] and "exec_lm_core LM_robustness->raise_error: Test exception" in output[1]:
        return True, f'{info_msg}: Valid error msg: exec_lm_core *->raise_error: *'
    else:
        return False, f'{info_msg}: {output}'


def check_robustness_memory():
    info_msg = '[ST] Check robustness - memory_leak [robustness memory_leak 12]'
    print(info_msg)
    cmd_list = ['robustness memory_leak 12']
    output = execute(cmd_list)
    if output[0] and "[12] RAM Alloc" in output[1]:
        end_result = output[1].split("\n")[-1]
        return True, f'{info_msg}: Mem alloc: {end_result}'
    else:
        return False, f'{info_msg}: {output}'


def check_robustness_recursion():
    info_msg = '[ST] Check robustness - recursion [robustness recursion_limit 5]'
    print(info_msg)
    cmd_list = ['robustness recursion_limit 5']
    output = execute(cmd_list, tout=10)
    if output[0]:
        last_line = output[1].split("\n")[-1]
        if "Recursion limit:" in last_line:
            info_msg += f'-> {last_line}'
            return True, f'{info_msg}'
    return False, f'{info_msg}: {output}'


def check_intercon(host=None):
    def _convert_return_to_dict(data):
        try:
            data_dict = ast.literal_eval(data[1])
        except Exception as e:
            data_dict = {'tag': None, 'verdict': f'{data}: {str(e)}'}
        return data[0], data_dict

    def _get_intercon_output(tag):
        _cmd_list = [f'task show {tag}']
        _state = False
        _output = None
        for _ in range(0, 2):
            time.sleep(1)
            _output = execute(_cmd_list, tout=8)
            if _output[0] and 'No task found:' not in _output[1]:
                _state = True
                break
        return _state, _output

    info_msg = '[ST] Check device-device connectivity'
    print(info_msg)
    host = 'test.local' if host is None else host
    cmd_list = ['intercon sendcmd "{}" "hello" >json'.format(host)]
    output = execute(cmd_list, tout=8)
    output = _convert_return_to_dict(output)
    device_was_found = False
    if output[0] is False or output[1] is None:
        output = 'Device was not found: {}:{}'.format(host, output)
        return False, output
    elif output[1] == '[]':
        # Valid input, device was not found
        output = 'Device was not found: {}:{}'.format(host, output)
        state = True, f'{info_msg}:\n\t\t{output}'
    elif len(output[1]) > 1 and "hello" in output[1]['verdict']:
        response_state, response = _get_intercon_output(output[1]['tag'])
        # Valid input on online device
        output = "Device was found: {}:{}".format(host, f"{output}: {response}")
        state = True & response_state, f'{info_msg}:\n\t\t{output}'
        device_was_found = True
    else:
        state = False, output

    if device_was_found:
        # DO Negative testing as well
        cmd_list = ['intercon sendcmd "notavailable.local" "hello" >json']
        output_neg = execute(cmd_list, tout=15)
        output_neg = _convert_return_to_dict(output_neg)
        state_neg = False, output_neg
        if len(output_neg[1]) > 1 and "hello" in output_neg[1]['verdict']:
            response_state, response = _get_intercon_output(output_neg[1]['tag'])
            output_neg = f'Device was not found: "notavailable.local":{output_neg}: {response}'
            state_neg = True & response_state, output_neg
        return state[0] & state_neg[0], "{}\n\t\tNegative test: {}".format(state[1], state_neg[1])
    return state


def measure_conn_metrics():
    try:
        verdict = socketClient.connection_metrics(f"{get_device().strip()}.local")
        for k in verdict:
            print("\t\t{}".format(k))
        state = True if len(verdict) > 0 else False
    except Exception as e:
        state = False
        verdict = [str(e), '']
    return state, f'{" "*51}'.join(verdict)


def memory_usage():
    cmd = ['system memory_usage >json']
    out = execute(cmd, tout=3)
    state, raw_output = out[0], out[1]
    try:
        json_out = json.loads(raw_output)
    except Exception as e:
        return False, '[ST] {}ERR{}: {}: {}'.format(Colors.ERR, Colors.NC, raw_output, e)

    # {"percent": 93.11, "mem_used": 103504}
    if json_out.get('percent') > 80:        # MEM USAGE WARNING INDICATOR: 85%
        return state, '[ST] {}WARNING{}: memory usage {}% ({} bytes)'.format(Colors.WARN, Colors.NC,
                                                                             json_out.get('percent'),
                                                                             json_out.get('mem_used'))
    return state, '[ST] {}OK{}: memory usage {}% ({} bytes)'.format(Colors.OK, Colors.NC,
                                                                    json_out.get('percent'), json_out.get('mem_used'))


def disk_usage():
    """
    Check disk usage - manually defined 16% (336_000 byte) - check degradations...
    """
    cmd = ['system disk_usage >json']
    out = execute(cmd, tout=3)
    state, raw_output = out[0], out[1]
    try:
        json_out = json.loads(raw_output)
    except Exception as e:
        return False, '[ST] {}ERR{}: {}: {}'.format(Colors.ERR, Colors.NC, raw_output, e)

    # {"percent": 15.4, "fs_used": 323_584}
    if json_out.get('fs_used') > 500_000:        # MEM USAGE WARNING INDICATOR: 500_000 bytes (500kb)
        return state, '[ST] {}WARNING{}: disk usage {}% ({} bytes)'.format(Colors.WARN, Colors.NC,
                                                                             json_out.get('percent'),
                                                                             json_out.get('fs_used'))
    return state, '[ST] {}OK{}: disk usage {}% ({} bytes)'.format(Colors.OK, Colors.NC,
                                                                  json_out.get('percent'), json_out.get('fs_used'))


def task_list():
    cmd = ['task list']
    out = execute(cmd, tout=3)
    state, output = out[0], out[1]
    if state:
        return state, output.replace('\n', f'\n{" "*51}')        # TODO format output
    return state, output


def webcli_test():
    endpoints = []
    cmd = ['conf', 'webui']
    out = execute(cmd, tout=3)
    state, output = out[0], out[1]
    if state:
        verdict = f"[ST] WEBUI IS ENABLED ({output})" if output.strip() == 'True' else f"[ST] WEBUI IS DISABLED ({output})"
        if output.strip() == 'True':
            out = execute(['conf', 'devip'], tout=3)
            if out[0] and out[1] is not None:
                devip = out[1]
                endpoints.append(f'http://{devip}')
                endpoints.append(f'http://{devip}/rest')

            for endpoint in endpoints:
                _start_t = time.time()
                try:
                    response = requests.get(endpoint, timeout=5)
                    # Check if the request was successful
                    if not (response.status_code == 200 and ('<!DOCTYPE html>' in str(response.content) or '"micrOS"' in str(response.content))):
                        verdict += f" Endpoint: {endpoint} [{Colors.ERR}NOK{Colors.NC}]({round(time.time()-_start_t, 2)}s)"
                        print(response.content)
                        state = False
                    else:
                        verdict += f" Endpoint: {endpoint} [{Colors.OK}OK{Colors.NC}]({round(time.time()-_start_t, 2)}s)"
                except Exception as e:
                    verdict += f" Endpoint: {endpoint} [{Colors.ERR}NOK{Colors.NC}]({round(time.time()-_start_t, 2)}s)"
                    print(f"webcli_test error: {e}")
                    state  = False
        return state, verdict
    return state, output


def app(devfid=None):
    global DEVICE
    if devfid is not None:
        DEVICE = devfid

    # Get test verdict
    verdict = {'single_cmds': single_cmd_exec_check(),
               'lm_cmd_exec': lm_cmd_exec_check(),
               'config_get': micrOS_config_get(),
               'config_set': micrOS_config_set(),
               'task_oneshot': micrOS_bgjob_one_shot_check(),
               'task_loop': micrOS_bgjob_loop_check(),
               'version': micrOS_get_version(),
               'json_check': json_format_check(),
               'reponse time': measure_package_response_time(),
               'negative_api': negative_interface_check(),
               'dhcp_hostname': check_device_by_hostname(DEVICE),
               'lm_exception': check_robustness_exception(),
               'mem_usage': memory_usage(),
               'disk_usage': disk_usage(),
               'webui_conn': webcli_test(),
               'mem_alloc': check_robustness_memory(),
               'recursion': check_robustness_recursion(),
               'intercon': check_intercon(host='RingLamp.local'),
               'micros_alarms': micros_alarm_check(),
               'conn_metrics': measure_conn_metrics(),
               'micros_tasks': task_list()
               }

    # Test Evaluation
    final_state = True
    ok_cnt = 0
    print(f"\n----------------------------------- micrOS System Test results on {DEVICE} device -----------------------------------")
    print("\tTEST NAME\t\tSTATE\t\tDescription\n")
    for test, state_data in verdict.items():
        state = Colors.ERR + 'NOK' + Colors.NC
        if state_data[0]:
            state = Colors.OK + 'OK' + Colors.NC
            ok_cnt += 1
        print(f"\t{test}:\t\t{state}\t\t[i]{state_data[1]}")
        final_state &= state_data[0]

    # Execution verdict
    pass_rate = round((ok_cnt/len(verdict.keys())*100), 1)
    print(f"\nPASS RATE: {pass_rate} %")
    state = 'OK' if final_state else 'NOK'
    colorful_state = Colors.OK + state + Colors.NC if state == 'OK' else Colors.WARN + state + Colors.NC
    print(f"RESULT: {colorful_state}")
    print("--------------------------------------------------------------------------------------\n")
    oled_msg_end_result(f"System[{state}] {pass_rate}")


def execute(cmd_list, tout=5):
    cmd_args = base_cmd() + cmd_list
    print("[ST] test cmd: {}".format(cmd_args))
    return socketClient.run(cmd_args, timeout=tout)


if __name__ == "__main__":
    app()
