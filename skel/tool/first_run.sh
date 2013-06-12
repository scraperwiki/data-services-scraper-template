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
    echo 'source ~/venv/bin/activate' >> ~/.bash_profile
fi

source venv/bin/activate
pip install -r requirements.txt

if [ "`crontab -l`" == "" ]; then
    crontab tool/crontab.txt
else
    echo "WARNING: not overwriting your existing crontab. You need to manually"
    echo "         run: crontab tool/crontab.txt"
fi

# Now we should have a working environment.
# 

# [ insert any scraper-specific initialisation code here ]

