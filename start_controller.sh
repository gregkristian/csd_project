# Dependencies are:
# ryu 4.6
# python 2.7
#
# Notes:
# No need to change PYTHONPATH env variable
RYU_CC_APP=controller_core_of10.py
LOG_FILE=/tmp/cclog.log
OUTPUT_LOG=/tmp/cc.log

#ryu-manager --observe-links --verbose --log-file $LOG_FILE --default-log-level 3 $RYU_CC_APP &> $OUTPUT_LOG & 

ryu-manager --observe-links --install-lldp-flow  --verbose --log-file $LOG_FILE --default-log-level 3 $RYU_CC_APP &> $OUTPUT_LOG & 

echo The log files are $LOG_FILE and $OUTPUT_LOG
echo tail -f anyone of them
