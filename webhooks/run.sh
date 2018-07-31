#!/bin/bash
#yangy114 20180112

runtime=`date "+%Y-%m-%d_%H%M%S"`
nohup python webhooks.py > ~/log/webhooks_log_$runtime 2>&1 &

# kill
# ps -ef | grep webhooks.py |awk '{print $2}' | xargs kill -9
