# -*- coding: utf-8 -*-
import requests

from lettuce import step, world
from nose.tools import assert_equals

from tornado.escape import json_encode

@step(u'I index note through handlers with text "([^"]*)"')
def i_index_note_through_handlers_with_text_group1(step, content):
    if not hasattr(world, "index_posts"):
        world.count = 1
    data = {
        "doc": {
            "id": world.count,
            "content": content,
            "tags": ["all"],
            "title": "Node {count}".format(count = world.count),
            "docType": "Note"
        },
        "fields": ["content", "title"]
    }
    world.count += 1
    response = requests.post("http://localhost:8888/index/",
                             data=json_encode(data))
    if not hasattr(world, "index_posts"):
        world.index_posts = list()
    world.index_posts.append(data["doc"])
    assert_equals(200, response.status_code)

@step(u'When I send a request to search the notes containing "([^"]*)"')
def when_i_send_a_request_to_search_the_notes_containing_group1(step, query):
    data = {
        "docType":"Note",
        "query": query
    }
    world.response = requests.post("http://localhost:8888/search/",
                                   data=json_encode(data))
    assert_equals(200, world.response.status_code)

@step(u'Then this note is the second note I created')
def then_this_note_is_the_second_note_i_created(step):
    assert_equals(world.response.json()["ids"][0],
                  unicode(world.index_posts[1]["id"]))

@step(u'Given I delete the second note index')
def given_i_delete_the_second_note_index(step):
    response = requests.delete("http://localhost:8888/index/2/")
    assert_equals(204, response.status_code)

@step(u'Then there is no result')
def then_there_is_no_result(step):
    assert_equals(len(world.response.json()["ids"]), 0)
