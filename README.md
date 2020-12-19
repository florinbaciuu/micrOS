# ![LOGO](https://github.com/BxNxM/MicrOs/blob/master/media/logo_mini.png?raw=true) micrOS

### micropython based IoT framework for wifi capable arm based microcontrollers and much more...

### KEY PRINCIPLES:
✉️ 📡 Generic communication API -> Human / Machine interface <br/>
📲 💻 Custom built-in socket shell for configuration and execution <br/>
⚙️ 📝 Automatic device initialization from user config ;) <br/>
🚪 No external server / service required <br/>
⚠️ 🛡 Privacy in focus, works on Local Private Network <br/>
🧩  Codeless end user experience via phone client <br/>
🛠🦾 Easy to customize aka create Load Modules, copy **LM**\_your_app**.py** or **.mpy** to the device and call any function from your module.<br/>
🚀🎈Lightweight and high performance core system that leaves you space 😎<br/>

### QUICK LINKS:
1. micrOS Client Application [link](https://github.com/BxNxM/micrOS#ios--android-application)
2. micrOS Installer [link](https://github.com/BxNxM/micrOS#micros-toolkit-for-pc)
3. micrOS System and features [link](https://github.com/BxNxM/micrOS#micros-system-message-function-visualization)
4. micrOS Node configuration [link](https://github.com/BxNxM/micrOS#micros-node-configuration-parameters-with-description)
5. micrOS Tutorials [link](https://github.com/BxNxM/micrOS#micros-tutorial)

----------------------------------------

## iOS / Android Application

> Coming soon

![MICROSVISUALIZATION](./media/appGUI.gif?raw=true)

----------------------------------------

## Installing micrOS with DevToolKit from macOS / Windows / Linux

That repo not only contains the micrOS core codes provide several tools like

- Install new device via USB
- Device scan
- OTA updates (over wifi)
- Host side python app execution with device communication
- etc.

> Note: The main purpose to install micropython on the board and put all micrOS resources from micrOS/mpy-MicrOS to the board.

### 1. Clone **micrOS** repo:

Contains code for the supported boards for installation, the development, deployment and server tools, all written in python.

> Note: Install git manually for Windows before this step

```
git clone https://github.com/BxNxM/micrOs.git
```

### 2. Download python 3.8

Link for python 3.8 [download](https://www.python.org/downloads/release/python-383/)

> Note: Allow extend system path with that python version (installatiuon parameter)

### 3. Install serial driver for board connection via USB

Find the required driver in the cloned repo.

- For Windows
	
```
micrOs/driver_cp210x/CP210x_Universal_Windows_Driver
```
	
- For macOS
	
```
micrOs/driver_cp210x/SiLabsUSBDriverDisk.dmg
```

### 4. ONLY ON WINDOWNS: Special dependencies

	You will need C++ compiler to able to install all python pip dependencies (defined in the tool/requirements.txt)
	
	```
	Link for download: TODO
	```

### 5. Execute **devToolKit** GUI

It will open a graphical user interface for micrOS device management.

```
python3 micrOS/devToolKit.py
```

- Verified OS list for development and deployment:
	- macOS
	- Raspbian (pyQT5 limitation)
	- Windows (Precompiled code install on new devices okay, other features coming soon)

	
- Example

```
1. Select BOLAD TYPE
2. Select MICROPYTHON VERSION
3. Click on [Deploy (USB)] button
```

It will install your board via USB with default settings. Continue with your mobile app...  

![MICROSVISUALIZATION](./media/micrOSToolkit.gif?raw=true)

----------------------------------------

## micrOS System, message-function visualization 

![MICROSVISUALIZATION](./media/micrOS.gif?raw=true)

>Note: **Python Socket Client** for application development also available besides smartphone application (example below).


----------------------------------------

## micrOS Framework Features💡

- **micrOS loader** - micrOS / WEBREPL (update / recovery)
	- **OTA update** - push update over wifi (webrepl automation) with auto restart node
- **Config handling(*)** - node_config.json [socket access]
- **Boot phase** handling - preload modules - I/O initialization from node_config
- **Network handling** - based on node_config 
	- STA / AP
	- NTP setup
	- static IP configuration
- **Socket interpreter** - wireless communication interface with the devices/nodes
	- **System commands**: `help, version, reboot, webrepl, etc.`
		- webrepl <--> micrOS interface switch  
	- **Config(*)** SET/GET/DUMP
	- **LM** - Load Module function execution (application modules)
- **Scheduling / External events** - Interrupt callback - based on node_config 
	- Time based
		- simple time "shot" trigger
		- cron "timeboxed" task pool logic
	- Event based
- Load Module **application** handling
	- Lot of built-in functions
	- Create your own module with 2 easy steps
		- Create a file in `MicrOS` folder like: `LM_<your_app_name>.py`
		- Copy your py file to the board `devToolKit.py -m` or `devToolKit.py -i` or `ampy

		
DevToolKit CLI feature:

- Socket client python plugin - interactive - non interactive mode


![micrOS project Pheriphery Support](./media/micrOSprojectPheriphery.png)</br>

----------------------------------------

## System Architecture 

![MICROSARCHITECTURE](https://github.com/BxNxM/MicrOs/blob/master/media/MicrOSArchitecture.png?raw=true)

> Secure Core (OTA static modules): `boot.py`, `micrOSloader.mpy`, `Network.mpy`

## Device Pinout

![MicrOSESP8266pinout](https://github.com/BxNxM/MicrOs/blob/master/media/NodeMCUPinOutESP8266.png?raw=true)

![MicrOSESP8266pinout](https://github.com/BxNxM/MicrOs/blob/master/media/NodeMCUPinOutESP32.png?raw=true)

### RELESE NOTE

|  VERSION (TAG) |    RELEASE INFO    |  MICROS CORE MEMORY USAGE  |  SUPPORTED DEVICE(S) | APP PROFILES | Load Modules  |     NOTE       |
| :----------: | :----------------: | :------------------------:   |  :-----------------: | :------------: | :------------:| -------------- |
|  **v0.1.0-0** | [release_Info-0.1.0-0](https://github.com/BxNxM/MicrOs/tree/master/release_info/micrOS_ReleaseInfo/release_0.1.0-0_note.md)| 13 - 28 % (1216-2544byte) | esp8266 | [App Profiles](https://github.com/BxNxM/MicrOs/tree/master/release_info/node_config_profiles) | [LM manual](https://github.com/BxNxM/MicrOs/tree/master/release_info/micrOS_ReleaseInfo/release_sfuncman_0.1.0-0.json)| Stable Core with applications - first release
|  **v0.4.0-0** | [release_Info-0.4.0-0](https://github.com/BxNxM/MicrOs/tree/master/release_info/micrOS_ReleaseInfo/release_0.4.0-0_note_esp8266.md)| 26 - 53 % (2512-5072byte) | esp8266 | [App Profiles](https://github.com/BxNxM/MicrOs/tree/master/release_info/node_config_profiles) | [LM manual](https://github.com/BxNxM/MicrOs/tree/master/release_info/micrOS_ReleaseInfo/release_sfuncman_0.4.0-0.json)| micrOS multi device support with finalized core and so more. OTA update feature.
|  **v0.4.0-0** | [release_Info-0.4.0-0](https://github.com/BxNxM/MicrOs/tree/master/release_info/micrOS_ReleaseInfo/release_0.4.0-0_note_esp32.md)| 23 - 28 % (17250-20976byte) | esp32 | [App Profiles](https://github.com/BxNxM/MicrOs/tree/master/release_info/node_config_profiles) | [LM manual](https://github.com/BxNxM/MicrOs/tree/master/release_info/micrOS_ReleaseInfo/release_sfuncman_0.4.0-0.json)| micrOS multi device support with finalized core and advanced task scheduler based on time, and and so more. OTA update feature.

----------------------------------------

## MicrOS Tutorial

> **Coming soon - youtube channel**

- [1] How to deploy device
	- Windows / Mac tutorial
- [2] How to OTA update device
	- Windows / Mac tutorial
- [3] Widgets and Load Modules via micrOS Client  
	- How to get available module list
	- Overview of micrOS Client UI
- [4] Configuration via micrOS Client
	- Idea behind: network, time, boothook, irqs, cron
	- Set some stuff in config ...
- [5] Get familier with micrOS shell
	- micrOS terminal
	- built-in commands, Load Modules
- [6] How to develop with micrOS
	- Create custom Load Modules (LMs)

> **Coming soon**

----------------------------------------

## micrOS **node configuration**, parameters with description

| Parameters names |   Default value and type    | Reboot required |          Description            |
| ---------------- | :-------------------------: | :-------------: | ------------------------------- |
| devfid           |    `node01`  `<str>`        |       No        | Device friendly "unique" name - also used for AccessPoint nw mode (AP name)
| boostmd          |      `True`  `<bool>`       |     Yes         | boost mode - set up cpu frequency low or high 8MHz-16Mhz-24MHz (depends on boards)
| staessid         |   `your_wifi_name` `<str>`  |       Yes       | Wifi router name (for default connection mode)
| stapwd           | `your_wifi_passwd` `<str>`  |       Yes       | Wifi router password (for default connection mode)
| appwd            |   `ADmin123`  `<str>`       |       Yes       | Device system password.: Used in AP password (access point mode) + webrepl password
| gmttime          |     `1`   `<int>`          |        Yes       | NTP - RTC - timezone setup (GMT)
| boothook         |    `n/a` `<str>`            |      Yes        | Callback function(s) list for priority Load Module(s) execution in boot sequence [before network setup!]. Add LoadModule(s) here, separator `;`. Example: Set LED colors / Init custom module(s) / etc.
| timirq           |     `False`  `<bool>`       |       Yes       | Timer interrupt enabler - background "subprocess" emulation, timer based infinite loop for the LoadModule execution
| timirqcbf        |      `n/a`   `<str>`        |      Yes        | if `timirq` enabled, calls the given Load Module, e.x.: `module function optional_parameter(s)`
| timirqseq        |    `3000`   `<int>`         |      Yes        | Timer interrupt period in ms, default: `3000` ms (for `timirq` infinite loop timer value)
| cron             |     `False`  `<bool>`       |       Yes       | Cron enabler, time based task scheduler. (Requires enabled `timirq`)
| crontasks        |     `n/a`  `<str>`          |       Yes       | Cron scheduler input, task format: `WD:H:M:S!module function` e.g.: `1:8:0:0!system heartbeat`, task separator in case of multiple tasks: `;`. [WD:0-6, H:0-23, M:0-59, S:0-59] in case of each use: `*`
| extirq           |     `False`  `<bool>`       |      Yes        | External event interrupt enabler - Triggers when "input signal upper edge detected" - button press happens
| extirqcbf        |     `n/a`  `<str>`          |      Yes        | `extirq ` enabled, calls the given Load Module, e.x.: `module function optional_parameter(s)`
| pled             |     `True`    `<bool>`      |      Yes        | Progress led enabler - light pulse under processing - "heart beat"
| dbg	            |     `True`    `<bool>`      |       Yes       | Debug mode - enable micrOS system printout, server info, etc.
| soctout          |   `100`      `<int>`        |       Yes       | Socket server connection timeout (because single process socket interface)
| socport          |    `9008`  `<int>`          |       Yes       | Socket server service port (should not be changed due to client and API inconpatibility)
| irqmreq          |      `6000`  `<int>`        |      No         | Controlls memory overload avoidance (byte). `timirq` requires this amount of memory for activation. `irqmreq`*0.7 is the memory limit for `extirq` enabling. **WARNING**: If the system gets memory overloaded with irq(s) micropython crashes and stucks in cycling reboot!!!
| irqmembuf        |    `1000` `<int>`           |       Yes       | IRQ emergency memory buffer allocation (in byte) when `timirq` or `exitirq` enabled.
| devip            |      `n/a`  `<str>`         |       N/A       | Device IP address, (first stored IP in STA mode will be the device static IP on the network), you are able to provide specific static IP here.
| nwmd             |     `n/a`  `<str>`          |       N/A       | USED BY SYSTEM (state storage) - system saves network mode here - `AP` or `STA`
| hwuid            |      `n/a`  `<str>`         |       N/A       | USED BY SYSTEM (state storage) - hardware address - dev uid


> **Note**: To enabling `cron` scheduler - hardware interrupt must be enabled `timirq` (for cron logic sampling), perid will be `timirqseq`
> Note: Default empty value: n/a in case of string parameter.

## Logical pin association

[MicrOS/LogicalPins.py](https://github.com/BxNxM/MicrOs/blob/master/MicrOS/LogicalPins.py)

```
'builtin': 16,    # BUILT IN LED - progress_led
'pwm_0': 15,      # D8 - servo
'pwm_1': 13,      # D7 - pwm_red
'pwm_2': 2,       # D4 - pwm_green / servo2
'pwm_3': 0,       # D3 - pwm_blue / neopixel
'i2c_sda': 4,     # D2 - OLED
'i2c_scl': 5,     # D1 - OLED
'pwm_4': 12,      # D6 - extirqpin
'simple_0': 16,   # D0 - dist_trigger
'pwm_5': 14,      # D5 - dist_echo
'simple_1': 10,   # SD3 - dht_pin
'adc_0': 0,       # ADC0 - CO2
'simple_2': 9     # SD2 - PIR
```

----------------------------------------

## Developer Quick guide

#### Erase device & Deploy micropython & Install micrOS 

Go to micrOS repo, where the `devToolKit.py` located.

```
cd micrOs 
./devToolKit.py --make
```
> Note: Follow the steps :)


Search and Connect to the device

```
./devToolKit.py -s -c
```

----------------------------------------

**User commands**

```
./devToolKit.py -h

optional arguments:
  -h, --help            show this help message and exit

Base commands:
  -m, --make            Erase & Deploy & Precompile (MicrOS) & Install (MicrOS)
  -r, --update          Update/redeploy connected (usb) MicrOS. - node config will be restored
  -c, --connect         Connect via socketclinet
  -o, --OTA				 OTA update, over wifi (webrepl)
  -p CONNECT_PARAMETERS, --connect_parameters CONNECT_PARAMETERS
                        Parameters for connection in non-interactivve mode.
```

**Search devices**

```
./devToolKit.py --search_devices

or

./devToolKit.py -s
```

**List discovered devices with status updates**

```
./devToolKit.py -stat

or

./devToolKit.py --node_status
```

Output:

```
       [ UID ]                [ FUID ]	[ IP ]		[ STATUS ]	[ MEMFREE ]	[ VERSION ]
420c0xf40x420x440xc420d6      Lamp	     10.0.1.12	ONLINE		4864 byte	0.1.0-0
420e00x980420x910xb420a2      airquality 10.0.1.50	ONLINE		3792 byte	0.0.9-27
420x500x204200x680x420f7      slim01	 10.0.1.157	ONLINE		890 byte    0.0.9-27	
```

**Developer commands**

```
Development & Deployment & Connection:
  -e, --erase           Erase device
  -d, --deploy          Deploy micropython
  -i, --install         Install MicrOS on micropython
  -l, --list_devs_n_bins
                        List connected devices & micropython binaries.
  -cc, --cross_compile_micros
                        Cross Compile MicrOS system [py -> mpy]
  -v, --version         Get micrOS version - repo + connected device.
  -ls, --node_ls        List micrOS node filesystem content.
  -u, --connect_via_usb
                        Connect via serial port - usb

Toolkit development:
  --dummy               Skip subshell executions - for API logic test.
```

## Socket terminal example - non interactive

### Identify device

```
./devToolKit.py -c -p '--dev slim01 hello'
Load MicrOS device cache: /Users/bnm/Documents/NodeMcu/MicrOs/tools/device_conn_cache.json
Activate MicrOS device connection address
[i]         FUID        IP               UID
[0] Device: slim01 - 10.0.1.73 - 0x500x20x910x680xc0xf7
Device was found: slim01
hello:slim01:0x500x20x910x680xc0xf7
```

### Get help

```
./devToolKit.py -c -p '--dev slim01 help'
Load MicrOS device cache: /Users/bnm/Documents/NodeMcu/MicrOs/tools/device_conn_cache.json
Activate MicrOS device connection address
[i]         FUID        IP               UID
[0] Device: slim01 - 10.0.1.73 - 0x500x20x910x680xc0xf7
Device was found: slim01
hello - default hello msg - identify device (SocketServer)
exit  - exit from shell socket prompt (SocketServer)
[CONF] Configure mode:
   configure|conf     - Enter conf mode
         Key          - Get value
         Key:Value    - Set value
         dump         - Dump all data
   noconfigure|noconf - Exit conf mod
[EXEC] Command mode:
   oled_128x64i2c
                 text
                 invert
                 clean
                 draw_line
                 draw_rect
                 show_debug_page
                 wakeup_oled_debug_page_execute
                 poweron
                 poweroff
   system
         memfree
         gccollect
         reboot
         wifirssi
         heartbeat
         time
   gpio
       RGB
       RGB_deinit
       Servo
       Servo_deinit
```
 
### Embedded config handler
 
```  
./devToolKit.py -c -p '--dev slim01 conf <a> dump'
Load MicrOS device cache: /Users/bnm/Documents/NodeMcu/MicrOs/tools/device_conn_cache.json
Activate MicrOS device connection address
[i]         FUID        IP               UID
[0] Device: slim01 - 10.0.1.73 - 0x500x20x910x680xc0xf7
Device was found: slim01
[configure] slim01
  stapwd    :  <your_wifi_password>
  gmttime   :  1
  nwmd      :  STA
  soctout   :  100
  timirq    :  True
  appwd     :  Admin123
  devfid    :  slim01
  extirq    :  True
  dbg       :  True
  timirqcbf :  oled_128x64i2c show_debug_page
  hwuid     :  0x500x20x910x680xc0xf7
  staessid  :  <your_wifi_name>
  devip     :  10.0.1.73
  extirqcbf :  oled_128x64i2c invert
  socport   :  9008
  pled      :  True
```

### Load Modules - User defined functions

```
./devToolKit.py -c -p '--dev slim01 system memfree'
Load MicrOS device cache: /Users/bnm/Documents/NodeMcu/MicrOs/tools/device_conn_cache.json
Activate MicrOS device connection address
[i]         FUID        IP               UID
[0] Device: slim01 - 10.0.1.73 - 0x500x20x910x680xc0xf7
Device was found: slim01
CPU[Hz]: 160000000
GC MemFree[byte]: 5552
```

## SocketClient

### Config:

```json
{
    "<UINIGUE ID - MAC ADDRESS (UID)>": [
        "<MICROS DEVIDE IP (DEVIP)>",
        "<MICROS DEVIDE MAC>",
        "<MICROS FRIENDLY NAME (FUID)>"
    ]
}
```

> NOTE: MUST TO HAVE DATA FOR CONNECTION: 
```
<MICROS DEVIDE IP (DEVIP)>
```

> All the other data can be dummy value :) 

#### Interactive mode

```
./devToolKit.py -c 
or
./devToolKit.py -connect
Load MicrOS device cache: /Users/bnm/Documents/NodeMcu/MicrOs/tools/device_conn_cache.json
Activate MicrOS device connection address
[i]         FUID        IP               UID
[0] Device: slim01 - 10.0.1.73 - 0x500x20x910x680xc0xf7
Choose a device index: 0
Device IP was set: 10.0.1.73
slim01 $  help
hello - default hello msg - identify device (SocketServer)
exit  - exit from shell socket prompt (SocketServer)
[CONF] Configure mode:
   configure|conf     - Enter conf mode
         Key          - Get value
         Key:Value    - Set value
         dump         - Dump all data
   noconfigure|noconf - Exit conf mod
[EXEC] Command mode:
   oled_128x64i2c
                 text
                 invert
                 clean
                 draw_line
                 draw_rect
                 show_debug_page
                 wakeup_oled_debug_page_execute
                 poweron
                 poweroff
   system
         memfree
         gccollect
         reboot
         wifirssi
         heartbeat
         time
   gpio
       RGB
       RGB_deinit
       Servo
       Servo_deinit
slim01 $  gpio RGB(0,0,0)
SET RGB
slim01 $  exit
Bye!
exit and close connection from ('10.0.1.7', 51733)
```

## Project structure

### MicrOS resources library

```
├── MicrOS
│   ├── ConfigHandler.py
│   ├── Hooks.py
│   ├── InterConnect.py
│   ├── InterpreterCore.py
│   ├── InterpreterShell.py
│   ├── InterruptHandler.py
│   ├── LogicalPins.py
│   ├── Network.py
│   ├── Scheduler.py
│   ├── SocketServer.py
│   ├── boot.py
│   ├── micrOS.py
│   ├── micrOSloader.py
│   ├── reset.py
```
> Note: Core MicrOS components

```
│   ├── LM_distance_HCSR04.py
│   ├── LM_light.py
│   ├── LM_motion_sensor.py
│   ├── LM_oled_128x64i2c.py
│   ├── LM_oled_widgets.py
│   ├── LM_servo.py
│   ├── LM_system.py
│   ├── etc...
```
> LM (Load Modules) - Application logic - accessable over socket server as a command

```
│   └── node_config.json
```
> Note: System description config

### MicrOS development tools library

```
├── devToolKit.py
├── tools
│   ├── MicrOSDevEnv
```
> Note: devToolKit wrapper resources for development, deployment, precompile, etc.

```
│   ├── nwscan.py
│   ├── socketClient.py
```
> Note: devToolKit wrapper socket based connection handling

```
├── user_data
│   ├── device_conn_cache.json
│   └── node_config_archive
```
> Note: User data dir: conatins node connection informations (devToolKit --search_devices) and deployed node config backups are here.


### MicrOS deployment resources

Precompiled components with the actual user configured config location

```
├── mpy-MicrOS
│   ├── ConfigHandler.mpy
│   ├── Hooks.mpy
│   ├── InterConnect.mpy
│   ├── InterpreterCore.mpy
│   ├── InterpreterShell.mpy
│   ├── InterruptHandler.mpy
│   ├── LM_bme280.mpy
│   ├── LM_co2.mpy
│   ├── LM_dht11.mpy
│   ├── LM_dht22.mpy
│   ├── LM_dimmer.mpy
│   ├── LM_distance_HCSR04.py
│   ├── LM_esp32.py
│   ├── LM_intercon.py
│   ├── LM_light.mpy
│   ├── LM_light_sensor.mpy
│   ├── LM_motion_sensor.py
│   ├── LM_neopixel.mpy
│   ├── LM_oled_128x64i2c.mpy
│   ├── LM_oled_widgets.mpy
│   ├── LM_ph_sensor.py
│   ├── LM_servo.mpy
│   ├── LM_switch.mpy
│   ├── LM_system.mpy
│   ├── LM_water_level.py
│   ├── LogicalPins.mpy
│   ├── Network.mpy
│   ├── Scheduler.mpy
│   ├── SocketServer.mpy
│   ├── boot.py
│   ├── micrOS.mpy
│   ├── micrOSloader.mpy
│   ├── node_config.json
│   └── reset.mpy
```

> Note: These resources will be copy to the micropython base.

### Release info and Application Profiles

```
├── release_info
│   ├── micrOS_ReleaseInfo
│   │   ├── release_0.1.0-0_note.md
│   │   ├── release_0.4.0-0_note_esp32.md
│   │   ├── release_0.4.0-0_note_esp8266.md
│   │   ├── release_sfuncman_0.1.0-0.json
│   │   └── release_sfuncman_0.4.0-0.json
│   └── node_config_profiles
│       ├── README.md
│       ├── catgame_profile-node_config.json
│       ├── catgame_profile_command_examples.txt
│       ├── default_profile-node_config.json
│       ├── default_profile_command_examples.txt
│       ├── dimmer_profile-node_config.json
│       ├── dimmer_profile_command_examples.txt
│       ├── heartbeat_profile-node_config.json
│       ├── heartbeat_profile_command_examples.txt
│       ├── lamp_profile-node_config.json
│       ├── lamp_profile_command_examples.txt
│       ├── neopixel_profile-node_config.json
│       └── neopixel_profile_command_examples.txt
```

> Note:  Under node_config_profiles you can find **configuration temaples**, named **profiles** (devenv automatically able to inject these under deployment) - there are also **command examples** for each application.

> **MicrOS_Release_Info** folder(s) conatins system verification logs like:
> 
> - bootup log with different configurations
> - application execution log
> - memory measurements

### Other project resoures 

```
├── apps
│   ├── AirQualityBME280_app.py
│   ├── AirQualityDHT22_CO2_app.py
│   ├── AnanlogLED_app.py
│   ├── CatGame_app.py
│   ├── Dimmer_app.py
│   ├── GetVersion_app.py
│   ├── NeopixelTest_app.py
│   ├── Template_app.py
├── etc...
```

----------------------------------------

## HINTS

- Save **screen** console buffer (**output**)
Press `ctrl + A :` and type `hardcopy -h <filename>`

- Create callgraph: [pycallgraph](http://pycallgraph.slowchop.com/en/master/)

- Convert PNG/JPG-s to GIF: `convert -delay 60 ./*.png mygif.gif`

- Build micropython with frozen resources: https://github.com/micropython/micropython/tree/master/ports/esp8266

- micrOS source code lines of code:

```bash

bnm@Bans-MBP:MicrOS$ core_files=($(ls -1 | grep '.py' | grep -v 'LM_')); all_line_codes=0; for coref in ${core_files[@]}; do content_lines_cnt=$(cat $coref | grep -v -e '^$' | wc -l); all_line_codes=$((all_line_codes+content_lines_cnt)); echo -e "$content_lines_cnt\t$coref"; done; echo -e "SUM OF CODE LINES: $all_line_codes"
     172	ConfigHandler.py
      51	Hooks.py
      41	InterConnect.py
      66	InterpreterCore.py
     155	InterpreterShell.py
     138	InterruptHandler.py
      45	LogicalPins.py
     158	Network.py
     126	Scheduler.py
     237	SocketServer.py
      16	boot.py
      53	micrOS.py
      97	micrOSloader.py
       5	reset.py
SUM OF CODE LINES: 1360

```

GIT:
- Add git tag: `git tag -a vX.Y.Z-K -m "tag message"`
	
- Publish tags: `git push origin --tags`
	
- Pretty git view: `git log --pretty=oneline`
	
- File change list: `git diff --name-only fbb4875609a3c0ee088b6a118ebf9f8a500be0fd HEAD | grep 'mpy-MicrOS'` 

git push -u origin master
