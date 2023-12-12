#!/bin/bash
#set -x

VERSION=$1
DEV=false
DEV_STR=''

if [[ "$VERSION" == "" ]]
then
    echo -e "Missing version number"
    echo -e "Hint:"
    echo -e "\t[1] param: new docker image version"
    echo -e "\tOR"
    echo -e "\t[1] param: dev (means create development image from repo - not pip)"
    echo -e "\t[2] param: new docker dev image version"
    exit 1
elif [[ "$VERSION" == "dev" ]]
then
    echo -e "DEVELOPMENT BUILD"
    DEV=true
    VERSION="$2"
    DEV_STR="-dev"
    if [[ "$VERSION" == "" ]]
    then
      echo -e "Missing version number"
      exit 1
    fi
else
    echo -e "$VERSION" >> versions.txt
fi

IMAGE="bxnxm/micros-gateway${DEV_STR}:${VERSION}"

echo -e "[CREATE IMAGE] DEV: ${DEV}"
if [[ "${DEV}" == "true" ]]
then
  # DEV BUILD
  echo -e "|------- docker build -t ${IMAGE} -f DockerfileDev"
  docker build -t "${IMAGE}" -f DockerfileDev .
else
  # PROD BUILD
  echo -e "|------- docker build --no-cache -t ${IMAGE}"
  docker build --no-cache -t "${IMAGE}" .
fi

echo -e "[RUN IMAGE] docker run"
docker run --name micros-gateway -p 5000:5000 -e GATEWAYIP="10.0.1.1" -d "${IMAGE}"


if [[ "${DEV}" == "false" ]]
then
  echo -n "DO YOU WANT TO PUBLISH THE IMAGE ${IMAGE} (Y/n): "
  read answer

  if [[ "$answer" == "Y" ]]; then
    echo -e "\t[PUBLISH CONTAINER] docker push "${IMAGE}""
    docker push "${IMAGE}"
  else
    echo -e "\t[PUBLISH CONTAINER] SKIP docker push "${IMAGE}""
  fi
fi

exit 0
