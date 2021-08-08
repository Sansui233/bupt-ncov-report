#!/bin/bash
function rand(){
    min=$1
    max=$(($2-$min+1))
    num=$(date +%s%N)
    echo $(($num%$max+$min))
}
rnd=$(rand 1 50)
echo "Sleep for ${rnd} minutes"
sleep ${rnd}m
export BUPT_SSO_USER=
export BUPT_SSO_PASS=
export SERVER_CHAN_SCKEY=
basepath=$(cd `dirname $0`; pwd)
python3 ${basepath}/main.py --stop-when-sick
