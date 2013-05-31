#!/bin/bash -ex
THIS_SCRIPT=`readlink -f $0`
SCRIPT_DIR=`dirname ${THIS_SCRIPT}`
TARGET_DIR=`readlink -f ${SCRIPT_DIR}/..`


function copy_skeleton_tool {
    cp -R skel/* ${TARGET_DIR}
}

function install_crontab {
    CRONTAB_FILE=${TARGET_DIR}/tool/crontab.txt
    sed -i "s|%TARGET_DIR%|${TARGET_DIR}|g" ${TARGET_DIR}/tool/crontab.txt
    crontab -l > ~/crontab.BAK
    crontab -i ${CRONTAB_FILE}
}

copy_skeleton_tool
install_crontab
