# -*- coding: utf-8 -*-

from lettuce import step, world
from nose.tools import assert_equals

from lib.indexer import Indexer

def createNote(id, title, content):
    note = dict()
    note["title"] = title
    note["content"] = content
    note["id"] = id
    note["tags"] = ["all"]
    return note

@step(u'Given I create five notes with tags and text')
def given_i_create_five_notes_with_tags_and_text(step):
    world.notes = []
    world.notes.append(
        createNote(1, "knights", "This a long story about knights"))
    world.notes.append(
        createNote(2, "faeries", "They battle for faeries and queens"))
    world.notes.append(
        createNote(3, "fight",
                   "But they don't know about karetaka or ninjutsu"))
    world.notes.append(
        createNote(4, "beasts",
                   "But this is useless versus dragon and witches"))
    world.notes.append(
        createNote(5, "master",
                "Hopefully they are master of vim that could impress anyone"))

@step(u'And I index them')
def and_i_index_them(step):
    world.indexer = Indexer()
    for note in world.notes:
        world.indexer.index_doc("Note", note, ["title", "content"])

@step(u'When I ask for search "([^"]*)"')
def when_i_ask_for_search_group1(step, word):
    world.ids = world.indexer.search_doc(unicode(word), ["Note"])

@step(u'It returns me the note about "([^"]*)"')
def it_returns_me_note_the_note_about_group1(step, group1):
    assert_equals(len(world.ids), 1)
    assert_equals(world.ids[0], unicode(world.notes[3]["id"]))

@step(u'Given I remove the note about "([^"]*)"')
def given_i_remove_the_note_about_group1(step, group1):
    world.indexer.remove_doc(world.ids[0])

@step(u'Then It returns nothing')
def then_it_returns_nothing(step):
    assert_equals(len(world.ids), 0)
