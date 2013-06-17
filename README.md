# Template layout for scrapers made by data services.

SSH into a fresh dataset, then run the following commands:

    mkdir ~/BAK && mv ~/tool ~/incoming ~/http ~/BAK
    git clone git@bitbucket.org:scraperwikids/data-services-scraper-template.git
    ./data-services-scraper-template/install.sh .

Now you have a brand new local git repo at the top level. It is safe to remove
the template repo with this command:

    rm -rf ./data-services-scraper-template

Now head over to BitBucket and create a new private repository for this
scraper:

https://bitbucket.org/repo/create

Select "I have an existing project to push up".

This will give you a 'git remote' command for linking the local repo to the
new remote repo - you should run this now.

Back in your box, edit ./README.md with the URL of the new repo in BitBucket.

Now do your initial commit and push to BitBucket:

    git add .
    git commit -m "Initial commit, template scraper."
    git push -u origin --all   # to push up the repo for the first time

Finally, activate your scraper (enable crontab, create virtualenv etc) by
running the following command:

    ./tool/first_run.sh
