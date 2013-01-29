servelife
==========

Alan and Anub building great stuff!

Git Branching
=============

For each feature or set of features, you should create a new branch. You
can do this by running 'git checkout -b branch_name'

When you're ready to merge your changes back into master, update master
and merge it into your branch. Here are the commands and how to get them
done.

    `git checkout master`
    `git pull`
    `git checkout my_branch`
    `git merge master`

This is where you handle any merge conflicts and commit the changes.

    `git checkout master`
    `git merge my_branch`

Then you can commit and push the merged changes.
