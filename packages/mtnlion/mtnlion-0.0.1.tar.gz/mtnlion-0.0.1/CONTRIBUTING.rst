.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://gitlab.com/macklenc/mtnlion/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitLab issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitLab issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Mountian Lion CSS could always use more documentation, whether as part of the
official Mountian Lion CSS docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://gitlab.com/macklenc/mtnlion/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up ``mtnlion`` for local development.

First, fork the mtnlion project into your personal account. This will give you a sandbox to play in that won't effect other users in any way. 
Then follow the instructions from the installation guide :doc:`installation`.

Every time you commit the pre-installed pre-commit hooks will evaluate your code for quality.
If any of the formatters report a failure, this means that they applied changes to your code and unstaged the relevant files.
You can then perform a git diff to view the changes the formatter made then re-add the files and try committing again.

When the feature or bug you've been working on in your forked repo is ready, you can submit a merge request to the upstream repo.
To do so, in the forked repo, go to Merge Requests and select the branch that you want to merge and select the ``devel`` branch in the upstream repo as the target.
Then follow the Merge Request Guidelines and fill out the Merge Request Template.

Merge Request Guidelines
------------------------

Before you submit a merge request, check that it meets these guidelines:

1. The merge request should include tests.
2. If the merge request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.6.

Tips
----

- To run a subset of tests::

    $ pytest tests.test_mtnlion

- Use pycharm! To setup pycharm simply import mtnlion and go to settings ``Ctrl+Alt+S`` then go to
  ``Project: mtnlion -> Project Interpreter``, click on the gear and select ``add``. Select ``existing interpreter``,
  and the system environment should be auto-discovered. Choose that and exit all menu's
  selecting "OK".


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed.

Then tag the release version providing a changelog in the annotation. Pushing the tag will trigger the pipeline to deploy
to GitLab releases, GitLab registry (for docker images), and PyPI
