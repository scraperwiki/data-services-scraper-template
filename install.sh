#!/bin/bash -e
THIS_SCRIPT=`readlink -f $0`
SCRIPT_DIR=`dirname ${THIS_SCRIPT}`

function copy_skeleton_tool {
    cp -R skel/* ${TARGET_DIR}
}

function install_crontab {
    CRONTAB_FILE=${TARGET_DIR}/tool/crontab.txt
    sed -i "s|%TARGET_DIR%|${TARGET_DIR}|g" ${TARGET_DIR}/tool/crontab.txt
    crontab -l > ~/crontab.BAK
    crontab -i ${CRONTAB_FILE}
}

function make_git_repo {
    pushd ${TARGET_DIR}
        git init
        git add .
    popd
}

function setup_virtualenv {
    virtualenv ${TARGET_DIR}/venv
}

function print_success_message {
    echo 'Success!'
    echo "Now edit ${TARGET_DIR}/README.md and do your initial commit."
}

function rename_gitignore_files {
    mv ${TARGET_DIR}/.gitignore.skel ${TARGET_DIR}/.gitignore
}

if [ "$#" -lt 1 ]; then
    echo
    echo "Usage: $0 <top-level directory>"
    echo
    echo "If you're in a new box, you probably want:"
    echo
    echo "$0 ~/"
    echo
    exit 1
else
    TARGET_DIR=`readlink -f $1`
fi

copy_skeleton_tool
install_crontab
make_git_repo
print_success_message

