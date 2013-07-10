#!/bin/bash -ex
THIS_SCRIPT=`readlink -f $0`
SCRIPT_DIR=`dirname ${THIS_SCRIPT}`

function copy_skeleton_dir {
    pushd skel/
    cp -R . ${TARGET_DIR}
    popd
}

function substitute_target_dir {
    CRONTAB_FILE=${TARGET_DIR}/tool/crontab.txt
    RUN_SH=${TARGET_DIR}/run.sh
    sed -i "s|%TARGET_DIR%|${TARGET_DIR}|g" ${CRONTAB_FILE} ${RUN_SH}
}


function rename_dotfiles {
    for filename in ${TARGET_DIR}/dotfile.*
    do
        new_filename=$(echo $filename | sed 's/dotfile././g')
        mv $filename $new_filename
    done
}

function make_git_repo {
    pushd ${TARGET_DIR}
        git init
        git add -f .gitignore
    popd
}

function print_success_message {
    echo
    echo 'Success!'
    echo "Now you have a brand new git new repo at ${TARGET_DIR}"
    echo
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
rename_dotfiles
make_git_repo
print_success_message

