#!/bin/bash -e
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

function make_git_repo {
    pushd ${TARGET_DIR}
        git init
    popd
}

function rename_dotfiles {
    for filename in ${TARGET_DIR}/dotfile.*
    do
        new_filename=$(echo $filename | sed 's/dotfile././g')
        mv $filename $new_filename
        git add -f $new_filename
    done
}

function print_success_message {
    echo
    echo 'Success!'
    echo "Now edit ${TARGET_DIR}/README.md and do your initial commit."
    echo
    echo "Activate the scraper with: ${TARGET_DIR}/tool/first_run.sh"
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
make_git_repo
rename_dotfiles
print_success_message

