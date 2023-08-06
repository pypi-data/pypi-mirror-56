#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `trello_release_notes` package."""

import pytest


from trello_release_notes.trello_release_notes import Trellist
from trello_release_notes.__main__ import get_arg_parser
from collections import namedtuple
from pathlib import Path

test_ini = Path("tests/trello_test_settings.ini")
args = None
if test_ini.exists():
    args = get_arg_parser().parse_args(["--config", str(test_ini)])
else:
    Args = namedtuple("Args", "apikey apisecret boardname done_list releases")
    from os import environ

    args = Args(
        environ["apikey"],
        environ["apisecret"],
        environ["boardname"],
        environ["done_list"],
        environ["releases"],
    )

boardname = args.boardname
done_name = args.done_list
expected_summary = """- card headline 0
- card headline 1
- card headline 2
- card headline 3"""

expected_members_summary = """- card headline 0 ['fo', 'ob', 'ar']
- card headline 1 
- card headline 2 ['fo', 'ob', 'ar']
- card headline 3 """

@pytest.fixture
def sample_cards():
    Card = namedtuple("Card", "name description url")
    samples = []
    for num in range(0, 4):
        samples.append(
            Card(
                f"card headline {num}",
                f"card description {num}",
                f"http://example.com/{num}",
            )
        )
    return samples

@pytest.fixture
def sample_member_cards():
    Card = namedtuple("Card", "name description url members_initials members_full_names members_usernames")
    samples = []
    for num in range(0, 4):
        members_initials = ""
        if num % 2 == 0:
            members_initials  = ["fo", "ob", "ar"]
        samples.append(
            Card(
                f"card headline {num}",
                f"card description {num}",
                f"http://example.com/{num}",
                members_initials,
                "",
                "",
            )
        )
    return samples

# scope at module level to avoid extra get_board calls
@pytest.fixture(scope="module")
def trellist():
    trellist = Trellist(
        args.apikey, args.apisecret, args.boardname, args.done_list, args.releases
    )
    return trellist

def test_summarize_these_cards(trellist, sample_cards):
    summary = trellist.summarize_these(sample_cards, template="- {card.name}", prep_function=lambda discard,x: x)
    assert expected_summary == summary

def test_summarize_these_cards_with_members(trellist, sample_member_cards):
    summary = trellist.summarize_these(sample_member_cards, template="- {card.name} {card.members_initials}", prep_function=lambda discard, x: x)
    assert expected_members_summary == summary


def test_get_board(trellist):
    # let's connect and get a board
    board = trellist.get_board(boardname)
    assert board is not None
    assert board.name == boardname


def test_get_list_by_name(trellist):
    trello_list = trellist.get_list_by_name(done_name)
    assert trello_list.name == done_name


def test_get_done_cards(trellist):
    # need to set up and insert done cards for the test
    for num in range(0, 4):
        trellist.done.add_card(f"card {num}", f"description {num}")
    done_cards = trellist.get_done_cards()
    # tear down - remove every card on the list
    trellist.done.archive_all_cards()
    assert len(done_cards) == 4


def test_create_release_card(trellist, sample_member_cards):
    trellist.prep_card = lambda discard, x: x
    card = trellist.create_release_card(sample_member_cards, trellist.release_template, trellist.card_summary_template)
    assert card.description == expected_members_summary
    expected_card_sample_count = "{}".format(len(sample_member_cards))
    count_from_name = card.name.split(" ")[2]
    card.delete()
    assert count_from_name == expected_card_sample_count


def test_add_comment_to_release(trellist, sample_cards):
    card = sample_cards[0]

    class ReleaseCard:
        def comment(self, text):
            self.comment_text = text

    rc = ReleaseCard()
    trellist.add_comment_to_release(rc, card)
    assert (
        rc.comment_text == "card headline 0\nhttp://example.com/0\ncard description 0"
    )
