# -*- coding: utf-8 -*-
import requests

from lettuce import step, world
from tornado.escape import json_encode, json_decode

class Client():
    def __init__(self, host="localhost:3000"):
        self.host = "http://%s/" % host

    def get(self, path, data):
        response = requests.get(self.host + path)
        return json_decode(response["data"])

    def post(self, path, data):
        response = requests.get(self.host + path, data=json_encode(data))
        return json_decode(response["data"])

    def put(self, path, data):
        response = requests.put(self.host + path, data=json_encode(data))
        return json_decode(response["data"])

client = Client()


@step(u'Send a request to check existence of Note with id equal to 123')
def send_a_request_to_check_existence_of_note_with_id_equal_to_123(step):
    data = {
        "id":123,
        "dataType":"Note",
    }
    world.response = client.post("exists/", data)

@step(u'Check that {exists: false} is returned')
def check_that_exists_false_is_returned(step):
    assert "exists" in world.response
    assert not world.response["exists"]

@step(u'Send a request to create a note')
def send_a_request_to_create_a_note(step):
    data = {
        "id":123,
        "dataType":"Note",
        "title":"Test note 01",
        "content":"test content 01"
    }
    world.newNote = client.post("create/", data)

@step(u'Send a request to check existence of Note with id equal to note ID')
def send_a_request_to_check_existence_of_note_with_id_equal_to_note_id(step):
    data = {
        "id": world.newNote["_id"],
        "dataType":"Note",
    }
    world.response = client.post("exists/", data)

@step(u'Check that {exists: true} is returned')
def check_that_exists_true_is_returned(step):
    assert "exists" in world.response
    assert world.response["exists"]



