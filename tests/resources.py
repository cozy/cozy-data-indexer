# -*- coding: utf-8 -*-
import requests

from lettuce import step, world
from nose.tools import assert_equals

from tornado.escape import json_encode

import logging
logger = logging.getLogger('tests.' + __name__)

@step(u'I index note through handlers with text "([^"]*)"')
def i_index_note_through_handlers_with_text_group1(step, content):
    if not hasattr(world, "index_posts"):
        world.count = 1
    data = {
        "doc": {
            "id": world.count,
            "content": content,
            "tags": ["all"],
            "title": "Note {count}".format(count = world.count),
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

    # resets the counter for a new scenario
    world.count = 1
    world.index_posts = list()

@step(u'Given I delete the second note index')
def given_i_delete_the_second_note_index(step):
    response = requests.delete("http://localhost:8888/index/2/")
    assert_equals(204, response.status_code)

@step(u'Then there is no result')
def then_there_is_no_result(step):
    assert_equals(len(world.response.json()["ids"]), 0)


@step(u'When I search the notes containing "([^"]*)" with option to show number of matched results')
def when_i_search_the_notes_containing_group1_with_option_to_show_number_of_matched_results(step, query):
    data = {
        "docType":"Note",
        "query": query,
        'showNumResults': True
    }
    world.response = requests.post("http://localhost:8888/search/",
                                   data=json_encode(data))
    assert_equals(200, world.response.status_code)

@step(u'Then the result is an object with fields, the notes and the number of results')
def then_the_result_is_an_object_with_fields_the_notes_and_the_number_of_results(step):

    response = world.response.json()
    assert u'ids' in response
    assert u'numResults' in response

@step(u'When I search the notes containing "([^"]*)" in page "([^"]*)"')
def when_i_search_the_notes_containing_group1_in_page_group2(step, query, page):
    data = {
        "docType":"Note",
        "query": query,
        "numPage": int(page),
        "numByPage": 1
    }
    world.response = requests.post("http://localhost:8888/search/",
                                   data=json_encode(data))
    assert_equals(200, world.response.status_code)

    # there should only be one result per page, as requested
    response = world.response.json()
    assert_equals(len(response[u'ids']), 1)

@step(u'Then the result should be the note "([^"]*)"')
def then_the_result_should_be_the_note_group1(step, index):
    index = int(index)
    response = world.response.json()
    assert_equals(index, int(response[u'ids'][0]))

    # resets the counter for a new scenario
    world.count = 1
    world.index_posts = list()

@step(u'I index note through handler with text "([^"]*)", title "([^"]*)" and tag "([^"]*)"')
def given_i_index_note_through_handler_with_text_group1_title_group2_and_tag_group3(step, content, title, tag):
    if not hasattr(world, "index_posts"):
        world.count = 1
    data = {
        "doc": {
            "id": world.count,
            "content": content,
            "tags": [tag],
            "title": title,
            "docType": "Note"
        },
        "fields": ["content", "title"],
        "fieldsType": {"content": "string", "title": "string"}
    }
    world.count += 1
    response = requests.post("http://localhost:8888/index/",
                             data=json_encode(data))
    if not hasattr(world, "index_posts"):
        world.index_posts = list()
    world.index_posts.append(data["doc"])

    assert_equals(200, response.status_code)

@step(u'Then all the notes should be in the results')
def then_all_the_notes_should_be_in_the_results(step):
    response = world.response.json()
    assert_equals(len(response['ids']), 3)

    # resets the counter for a new scenario
    world.count = 1
    world.index_posts = list()

@step(u'When I search the notes containing "([^"]*)" in "([^"]*)" of type "([^"]*)"')
def when_i_search_the_notes_containing_group1_in_group2(step, query, field, fieldType):

    if len(fieldType) is not 0:
        fieldType = "_%s" % fieldType

    query = "%s%s:%s" % (field, fieldType, query)

    print query
    data = {
        "docType":"Note",
        "query": query,
    }
    world.response = requests.post("http://localhost:8888/search/",
                                   data=json_encode(data))
    assert_equals(200, world.response.status_code)


@step(u'Then the result should be note "([^"]*)"')
def then_the_result_should_be_note_group1(step, index):
    response = world.response.json()
    assert_equals(response['ids'][0], index)

    # resets the counter for a new scenario
    world.count = 1
    world.index_posts = list()

