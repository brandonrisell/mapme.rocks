#!/bin/bash

mkdir -p ${HOME}/.ssh

echo "${PUBLIC_KEY}" > ${HOME}/.ssh/id_rsa.pub
echo "${PRIVATE_KEY}" > ${HOME}/.ssh/id_rsa

chmod 700 ${HOME}/.ssh
chmod 600 ${HOME}/.ssh/id_rsa
chmod 644 ${HOME}/.ssh/id_rsa.pub

ssh -n -i ${HOME}/.ssh/id_rsa -o StrictHostKeyChecking=no -N ${COMPOSE_PARAMS} &