#!/bin/bash -e
THIS_SCRIPT=`readlink -f $0`
SCRIPT_DIR=`dirname ${THIS_SCRIPT}`

function copy_skeleton_dir {
    cp -R skel/* ${TARGET_DIR}
}

function substitute_target_dir {
    CRONTAB_FILE=${TARGET_DIR}/tool/crontab.txt
    RUN_SH=${TARGET_DIR}/run.sh
    sed -i "s|%TARGET_DIR%|${TARGET_DIR}|g" ${CRONTAB_FILE} ${RUN_SH}
}

function rename_gitignore_files {
    mv ${TARGET_DIR}/gitignore.skel ${TARGET_DIR}/.gitignore
}

function make_git_repo {
    pushd ${TARGET_DIR}
        git init
        git add .
    popd
}

function print_success_message {
    echo
    echo 'Success!'
    echo "Now edit ${TARGET_DIR}/README.md and do your initial commit."
    echo "You may want to run ${TARGET_DIR}/tool/first_run.sh"
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

cd ${SCRIPT_DIR}

copy_skeleton_dir
substitute_target_dir
rename_gitignore_files
make_git_repo
print_success_message

