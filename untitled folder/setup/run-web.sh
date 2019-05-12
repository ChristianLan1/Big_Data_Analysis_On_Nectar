#!/bin/bash

. ./unimelb-comp90024-group-69-openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=~/deployment_key.txt nectar.yaml
