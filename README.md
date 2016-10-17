# Template layout for scrapers made by data services.

## Install

SSH into a fresh dataset, then run the following commands:

    mkdir ~/BAK && mv ~/tool ~/incoming ~/http ~/BAK
    git clone git@bitbucket.org:sensiblecode/data-services-scraper-template.git
    ./data-services-scraper-template/install.sh .

Now you have a brand new local git repo at the top level. It is safe to remove
the template repo with this command:

    rm -rf ./data-services-scraper-template

Now head over to BitBucket and create a new private repository for this
scraper:

[https://bitbucket.org/repo/create](https://bitbucket.org/repo/create)

Select "I have an existing project to push up".

This will give you a 'git remote' command for linking the local repo to the
new remote repo - you should run this now.

Back in your box, edit ./README.md with the URL of the new repo in BitBucket.

Now do your initial commit and push to BitBucket:

    git status
    git push -u origin --all   # to push up the repo for the first time

Finally, activate your scraper (enable crontab, create virtualenv etc) by
running the following command:

    ./tool/first_run.sh

# Using the template

The entry point for your code is ``tool/main.py``. If you're scraping a single
type of data you should probably keep all the code in that one file.

Sample data lives in ``tool/sample_data`` and should encompass every type of
file that the code works on (if you think this is excessive, try debugging in
6 months when the site has changed and you don't know how it used to look...)

Tests live in ``tool/tests.py`` and can be invoked from the ``tool/`` directory
by running ``nosetests``.

Requirements live in ``requirements.txt`` which is automatically installed into
the virtualenv when you use ``tool/first_run.sh``

In production, you should use ``~/run.sh`` to actually invoke the code. It's
how cron runs the code, and deliberately takes no arguments so that you can
easily reproduce what cron does.

Be aware that ``run.sh`` redirects output to the ``log/`` directory (see
``~/log/latest`` and supresses stdout unless there's an error, ie your
program exits with a nonzero error code.

# Code best practice

You should try and stick to the convention of using a ``process(f)`` function
which takes a file-like object (ie a web-page) and yields ``OrderedDicts``
representing rows to save to the database.

Using file-like objects allows us to access ``process(f)`` from both 
``main.py`` and ``tests.py`` without having to load huge files into memory.

# Logging

You should favour ``logging.info(..)`` over ``print(..)`` as we use the logging
basic configuration by default.

Do use at least info and debug log levels appropriately throughout the code.

# Licence

Everything within this *template* repo is licenced according to the top-level
LICENCE file.

Any new scraper which is generated from this template can have its own licence.

By default this is the Sensible Code proprietary licence which lives within
the ``skel/`` directory.

The LICENCE file inside ``skel/`` is only a suggestion for scrapers built from
the template; it has no effect on *this* template repo.
