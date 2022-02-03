"""
Module is responsible for network configuration
dedicated to micrOS framework.
- STA / STA
- static IP configuration
- NTP clock setup in case of STA
- generate UID based on mac address
- network status expose to config

Designed by Marcell Ban aka BxNxM

https://docs.micropython.org/en/latest/library/network.html
"""
#################################################################
#                           IMPORTS                             #
#################################################################
from utime import sleep_ms
from binascii import hexlify
from network import AP_IF, STA_IF, WLAN
from machine import unique_id
from ConfigHandler import cfgget, cfgput
from Time import ntptime
from Debug import console_write, errlog_add

#################################################################
#                      NTP & RTC TIME SETUP                     #
#################################################################


def set_ntp_rtc():
    err = ''
    for _ in range(4 if cfgget('cron') else 2):
        try:
            ntptime(utc_shift=int(cfgget('gmttime')))
            return True
        except Exception as e:
            console_write("set_ntp_rtc errer.:{}".format(e))
            err = e
        sleep_ms(100)
    errlog_add("set_ntp_rtc error: {}".format(err))
    return False

#################################################################
#                   GET DEVICE UID BY MAC ADDRESS               #
#################################################################


def set_dev_uid():
    try:
        cfgput('hwuid', 'micr{}OS'.format(hexlify(unique_id()).decode('utf-8')))
    except Exception as e:
        errlog_add("set_dev_uid error: {}".format(e))


def get_mac():
    return hexlify(WLAN().config('mac'), ':').decode()

#################################################################
#                       SET WIFI STA MODE                       #
#################################################################


def __select_available_wifi_nw(sta_if, raw_essid, raw_pwd):
    """
    raw_essid: essid parameter, in case of multiple values separator is ;
    raw_pwd: essid pwd parameter,  in case of multiple values separator is ;
    return detected essid with corresponding password
    """
    for idx, essid in enumerate(raw_essid.split(';')):
        essid = essid.strip()
        # Scan wifi network - retry workaround
        for _ in range(0, 2):
            if essid in (wifispot[0].decode('utf-8') for wifispot in sta_if.scan()):
                console_write('\t| - [NW: STA] ESSID WAS FOUND: {}'.format(essid))
                return essid, str(raw_pwd.split(';')[idx]).strip()
            sleep_ms(1000)
    return None, ''


def set_wifi(essid, pwd, timeout=60):
    console_write('[NW: STA] SET WIFI STA NW {}'.format(essid))

    # Disable AP mode
    ap_if = WLAN(AP_IF)
    if ap_if.active():
        ap_if.active(False)
    del ap_if

    # Set STA and Connect
    sta_if = WLAN(STA_IF)
    sta_if.active(True)
    # Set custom DHCP hostname
    sta_if.config(dhcp_hostname=cfgget('devfid'))
    # Check are we already connected
    if not sta_if.isconnected():
        # Multiple essid and pwd handling with retry mechanism
        essid, pwd = __select_available_wifi_nw(sta_if, essid, pwd)

        # Connect to the located wifi network
        if essid is not None:
            console_write('\t| [NW: STA] CONNECT TO NETWORK {}'.format(essid))
            # connect to network
            sta_if.connect(essid, pwd)
            # wait for connection, with timeout set
            while not sta_if.isconnected() and timeout > 0:
                console_write("\t| [NW: STA] Waiting for connection... {} sec".format(timeout))
                timeout -= 1
                sleep_ms(500)
            # Set static IP - here because some data comes from connection. (subnet, etc.)
            if sta_if.isconnected() and __set_wifi_dev_static_ip(sta_if):
                sta_if.disconnect()
                del sta_if
                return set_wifi(essid, pwd)
        else:
            console_write("\t| [NW: STA] Wifi network was NOT found: {}".format(essid))
            return False
        console_write("\t|\t| [NW: STA] network config: " + str(sta_if.ifconfig()))
        console_write("\t|\t| [NW: STA] CONNECTED: " + str(sta_if.isconnected()))
    else:
        console_write("\t| [NW: STA] ALREADY CONNECTED TO {}".format(essid))
    cfgput("devip", str(sta_if.ifconfig()[0]))
    set_dev_uid()
    return sta_if.isconnected()


def __set_wifi_dev_static_ip(sta_if):
    console_write("[NW: STA] Set device static IP.")
    stored_ip = cfgget('devip')
    if 'n/a' not in stored_ip.lower() and '.' in stored_ip:
        conn_ips = list(sta_if.ifconfig())
        # Check ip type before change, conn_ip structure: 10.0.1.X
        if conn_ips[0] != stored_ip and conn_ips[-1].split('.')[0:3] == stored_ip.split('.')[0:3]:
            console_write("\t| [NW: STA] micrOS dev. StaticIP request: {}".format(stored_ip))
            conn_ips[0] = stored_ip
            try:
                # IP address, subnet mask, gateway and DNS server
                sta_if.ifconfig(tuple(conn_ips))
                return True     # was reconfigured
            except Exception as e:
                console_write("\t\t| [NW: STA] StaticIP conf. failed: {}".format(e))
                errlog_add("__set_wifi_dev_static_ip error: {}".format(e))
        else:
            console_write("[NW: STA][SKIP] StaticIP conf.: {} ? {}".format(stored_ip, conn_ips[0]))
    else:
        console_write("[NW: STA] IP was not stored: {}".format(stored_ip))
    return False   # was not reconfigured


#################################################################
#                    SET WIFI ACCESS POINT MODE                 #
#################################################################


def set_access_point(_essid, _pwd, _authmode=3):
    console_write("[NW: AP] SET AP MODE: {} - {} - auth mode: {}".format(_essid, _pwd, _authmode))

    sta_if = WLAN(STA_IF)
    if sta_if.isconnected():
        sta_if.active(False)

    ap_if = WLAN(AP_IF)
    ap_if.active(True)
    # Set WiFi access point name (formally known as ESSID) and WiFi authmode (3): WPA2-PSK
    try:
        console_write("[NW: AP] Configure")
        ap_if.config(essid=_essid, password=_pwd, authmode=_authmode)
    except Exception as e:
        console_write("[NW: AP] Config Error: {}".format(e))
        errlog_add("set_access_point error: {}".format(e))
    if ap_if.active() and str(ap_if.config('essid')) == str(_essid) and ap_if.config('authmode') == _authmode:
        cfgput("devip", ap_if.ifconfig()[0])
    console_write("\t|\t| [NW: AP] network config: " + str(ap_if.ifconfig()))
    set_dev_uid()
    return ap_if.active()

#################################################################
#              AUTOMATIC NETWORK CONFIGURATION                  #
#              IF STA AVAILABLE, IF NOT AP MODE                 #
#################################################################


def auto_network_configuration():
    for _ in range(0, 3):
        # SET WIFI (STA) MODE
        state = set_wifi(cfgget("staessid"), cfgget("stapwd"))
        if state:
            # Save STA NW mode
            cfgput("nwmd", "STA")
            # Set NTP - RTC
            set_ntp_rtc()
            # BREAK - STA mode successfully  configures
            break
        # SET AP MODE
        state = set_access_point(cfgget("devfid"), cfgget("appwd"))
        if state:
            # Save AP NW mode
            cfgput("nwmd", "AP")
            # BREAK - AP mode successfully  configures
            break
