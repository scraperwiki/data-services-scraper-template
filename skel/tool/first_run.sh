#!/bin/bash -e

# This is the one-liner tool which does any initialisation required to setup
# a freshly-installed scraper.
#
# Add your code at the end of the file.

THIS_SCRIPT=`readlink -f $0`
THIS_DIR=`dirname ${THIS_SCRIPT}`
REPO_DIR=${THIS_DIR}/..

cd ${REPO_DIR}
if [ ! -d "venv" ]; then
    virtualenv venv
fi

pip install requirements.txt

if [ "`crontab -l`" == "" ]; then
    crontab tool/crontab.txt
else
    echo "WARNING: not overwriting your existing crontab. You need to manually"
    echo "         run: crontab tool/crontab.txt"

# Now we should have a working environment.
# 

# [ insert installation code here ]

