#!/bin/bash

# Get command line arguments
CMD_ARGS=${*}
# Get current script path
MY_PATH="$(dirname "${BASH_SOURCE[0]}")"
# Create script global path variables
if [[ "${MY_PATH}" == "." ]]
then
  venv_path="${MY_PATH}/env/venv"
  activate="${venv_path}/bin/activate"
  requirements="${MY_PATH}/env/requirements.txt"
else
  venv_path="./${MY_PATH}/env/venv"
  activate="./${venv_path}/bin/activate"
  requirements="./${MY_PATH}/env/requirements.txt"
fi

# Calculate if pip install was done once
install_req=0

# Set command line colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

function console_log {
  message=$1
  echo -e "$message"
  echo -e "$message" >> "${MY_PATH}/micros.log"
}

function venv_create {
    # Parse venv path: set / as the delimiter
    #IFS='/'
    #read -ra list <<< "$venv_path"
    # Check path is exists
    if [[ -d "$venv_path" ]]
    then
        if [[ ! -d "$venv_path" ]]
        then
            console_log "${GREEN}Create venv: ./$venv_path${NC}"
            python3.8 -m venv "${venv_path}"
            "${venv_path}/bin/python3.8" -m pip install --upgrade pip
            install_req=1
        else
            install_req=0
        fi
    else
        console_log "${RED}Invalid path: ${venv_path}${NC}"
    fi
}

function venv_requirements {
    if [[ -f "${requirements}" ]]
    then
        console_log "${GREEN}Install requirements: ${requirements}${NC}"
        python3.8 -m pip install -r "${requirements}"
    else
        console_log "${RED}No requirements file: ${requirements}${NC}"
    fi
}

#################################
#               VENV            #
#################################

# Create virtual environment
console_log "${GREEN}CREATE MICROS DEVTOOLKIT VIRTUAL ENVIRONMENT${NC}"
venv_create


# Check if venv already active & auto deactivate
if [[ -n "${VIRTUAL_ENV}" ]]
then
    . "deactivate"
fi

# Activate venv
console_log "${GREEN}ACTIVATE VIRTUAL ENVIRONMENT: ${activate}${NC}"
source ${activate}

# Install requirements
if [[ -n "${VIRTUAL_ENV}" && "${install_req}" -eq 1 ]]
then
    console_log "${GREEN}Virtual env active: ${VIRTUAL_ENV}${NC}"
    venv_requirements
else
    console_log "Venv setup skipped: ${VIRTUAL_ENV}"
fi

#################################
#           DEVTOOLKIT          #
#################################

function help {
    echo -e "\n============================================================="
    echo -e "==                  HELP MSG FOR magic.bash                =="
    echo -e "============================================================="
    echo -e "env        :activate python virtual environment and exit"
    echo -e "gateway    :start micrOS gateway service over devToolKit.py"
    echo -e "gitclean   :cleans untracked files, with -f cleans ignored too"
    echo -e "<no param> :run devToolKit.py without params -> GUI\n"
}


# CMD ARGUMENT: env
if [[ -n "${CMD_ARGS[0]}" ]]
then

  if [[ "${CMD_ARGS[0]}" == "env" ]]
  then
      console_log "Source env only, skip devToolKit load"
  elif [[ "${CMD_ARGS[0]}" == "gateway" ]]
  then
      # Start devToolKit.py gateway service
      console_log "Source env and start rest api server aka gateway"
      python3.8 "${MY_PATH}/devToolKit.py" -gw
  elif [[ "${CMD_ARGS[0]}" == "gitclean" ]]
  then
      git clean -fd
      if [[ -n "${CMD_ARGS[1]}" && "${CMD_ARGS[1]}" == "all" ]]
      then
        git clean -fdx
      fi
    elif [[ "${CMD_ARGS[0]}" == "help" || "${CMD_ARGS[0]}" == "-h" ]]
    then
      help
    fi
else
    help
    # Start devToolKit.py GUI
    console_log "Start devToolKit: ${MY_PATH}"
    python3.8 "${MY_PATH}/devToolKit.py"
fi
