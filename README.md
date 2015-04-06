## Description

Little API that provides indexation and full-text search features to the Cozy
Cloud Platform. It is based on
[Whoosh](http://pythonhosted.org//Whoosh/index.html) a Python indexation library.

## Install / Hack

Get build dependencies

    sudo apt-get install python python-pip python-dev libxml2-dev libxslt1-dev

Setup your virtual environment:

    sudo pip install virtualenv
    virtualenv virtualenv
    . virtualenv/bin/activate

Install dependencies:

    pip install -r requirements/common.txt

Start the server:

    python server.py

## Contribution

* Bring Whoosh features to the REST API.
* Pick and solve an [issue](https://github.com/mycozycloud/cozy-data-indexer/issues)

## Tests

[![Build
Status](https://travis-ci.org/mycozycloud/cozy-data-indexer.png?branch=master)](https://travis-ci.org/mycozycloud/cozy-data-indexer)

Install development dependencies

    pip install -r requirements/dev.txt

Run tests

    lettuce tests

## License

Cozy Data Indexer is developed by Cozy Cloud and distributed under the AGPL v3 license.

## What is Cozy?

![Cozy Logo](https://raw.github.com/mycozycloud/cozy-setup/gh-pages/assets/images/happycloud.png)

[Cozy](http://cozy.io) is a platform that brings all your web services in the
same private space.  With it, your web apps and your devices can share data
easily, providing you with a new experience. You can install Cozy on your own
hardware where no one profiles you. 

## Community 

You can reach the Cozy Community by:

* Chatting with us on IRC #cozycloud on irc.freenode.net
* Posting on our [Forum](https://groups.google.com/forum/?fromgroups#!forum/cozy-cloud)
* Posting issues on the [Github repos](https://github.com/mycozycloud/)
* Mentioning us on [Twitter](http://twitter.com/mycozycloud)
