## Description

Little API that provides indexation and full-text search features to Cozy Cloud
Data System.

## Setup

Get build dependencies

    sudo apt-get install python python-pip python-dev lxml2-dev libxslt1-dev

Setup your virtual environment

    sudo pip install virtualenv
    virtualenv virtualenv
    . virtualenv/bin/activate

Install dependencies

    pip install -r requirements/common.txt
    pip install -r requirements/production.txt

Start

    python server.py

## Tests

[![Build
Status](https://travis-ci.org/mycozycloud/cozy-data-indexer.png?branch=master)](https://travis-ci.org/mycozycloud/cozy-data-indexer)

Install development dependencies

    pip install -r requirements/dev.txt

Run tests

    lettuce tests

# About Cozy

This app is part of the Cozy platform backend. Cozy is the personal
server for everyone. It allows you to install your every day web applications 
easily on your server, a single place you control. This means you can manage 
efficiently your data while protecting your privacy without technical skills.

More informations and hosting services on:
http://cozycloud.cc
