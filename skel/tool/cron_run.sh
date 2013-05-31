#!/bin/bash

DATE_NOW=$(date +%Y-%m-%d_%H-%M-%S)
STATUS_URL='https://beta.scraperwiki.com/api/status'
LOG_DIR=~/log

mkdir -p ${LOG_DIR}
LOG_FILE=${LOG_DIR}/${DATE_NOW}.log

ln -sf ${LOG_FILE} ${LOG_DIR}/latest

for command in 01_download.py 02_process.py
do
    # Run the command specified on the command line
    run-one ${command} >> ${LOG_FILE} 2>&1
    RETCODE=$?
    if [ ${RETCODE} != 0 ]; then
        echo "$@ exited with code: ${RETCODE}"
        cat ${LOG_FILE}
        curl --data "type=error" ${STATUS_URL} > /dev/null 2>&1
        exit
    fi
done


# delete logs older than a week
find ${LOG_DIR} -type f -iname '*.log' -mtime +7 -delete

