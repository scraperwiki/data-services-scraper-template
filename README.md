# Template layout for scrapers made by data services.

SSH into a fresh dataset, then run the following commands:

    mkdir ~/BAK && mv ~/tool ~/incoming ~/http ~/BAK
    git clone git@bitbucket.org:scraperwikids/data-services-scraper-template.git
    ./data-services-scraper-template/install.sh .

Now you have a brand new local git repo at the top level. It is safe to remove
the template repo with this command:

    rm -rf ./data-services-scraper-template

Now head over to BitBucket and create a new private repository for this
scraper. This will give you some commands for linking the local repo to
the new remote repo.

    https://bitbucket.org/repo/create

Back in your box, edit ./README.md with the name of the scraper and the URL of
the new repo in BitBucket.

Now do your initial commit and push to BitBucket:

    git add .
    git commit -m "Initial commit, template scraper."
    git push

Finally, activate your scraper (enable crontab, create virtualenv etc) by
running the following command:

    ./tool/first_run.sh
