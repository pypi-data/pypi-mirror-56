# -*- coding: utf-8 -*-

"""Main module."""
from datetime import date
from trello import TrelloClient
from loguru import logger
from functools import lru_cache

"""
# given a list of boards
# for each board
# given a "done" list
# given a "released" list
# if there are items in the done list,
    create a release card for this date in the releases list
# for each item in the done list
# get the release card for this date
# append the title as list item to the description of the release card
# add the title and details as a comment on the release card
# archive the done item
# post process - send an email or do something with the release detail
"""


class Trellist(object):
    """The main object - initialize and use run()

    :param apikey: Your api-key.
    :param apisecret: Your api secret token. Get it from a protected file that you don't commit. Keep it secret!
    :param boardname: Name of the board to work on.
    :param done_list_name: The name of the done list on your board. Only one.
    :param releases_list_name: The name of the list to put release cards on.
    :param create_comments: True by default. Create a comment on the release card for each done card
    :param create_release_if_zero_done: If nothing is done, should you make a sad empty release card?
    """

    def __init__(
        self,
        apikey,
        apisecret,
        boardname,
        done_list_name="done",
        releases_list_name="releases",
        create_release_if_zero_done=False,
        create_comments=True,
    ):
        self.client = TrelloClient(api_key=apikey, api_secret=apisecret)
        self.board = self.get_board(boardname)
        self.done = self.get_list_by_name(done_list_name)
        self.releases = self.get_list_by_name(releases_list_name)
        self.release_template = "{date} release: {count} done"
        self.card_summary_template = "- {card.name} {card.members_initials}"
        self.create_release_if_zero_done = create_release_if_zero_done
        self.create_comment_per_item = create_comments

    def run(self):
        """Runs through all the methods to perform the work"""
        logger.info(f"get all cards in the done board: {self.done.name}")
        cards = self.get_done_cards()
        logger.info(f"got {len(cards)} cards")
        if cards or self.create_release_if_zero_done:
            release_card = self.create_release_card(
                cards, self.release_template, self.card_summary_template
            )
            for card in cards:
                if self.create_comment_per_item:
                    self.add_comment_to_release(release_card, card)
                card.set_closed(True)
        logger.info("finished run")

    def get_board(self, board_name):
        """Gets the open board object by a name, otherwise raises an Error to
        let you know we don't have that board

        :param board_name: actual name of a board you have access to
        """
        board = self.first(
            self.client.list_boards(), lambda b: b.name == board_name and not b.closed
        )
        if board:
            return board
        raise ValueError(
            (
                "Couldn't find an open board named '{}'. Check the name in your"
                " trello - are there extra quote marks in this message?"
            ).format(board_name)
        )

    def get_list_by_name(self, name):
        """Iterate lists and get the first one matching the name passed in

        :param name: Name of a list on the board you've passed in
        """
        trello_list = self.first(self.board.list_lists(), lambda l: l.name == name)
        if trello_list:
            return trello_list
        raise ValueError(
            (
                "Couldn't find a list named '{}'. Check the name in your trello"
                " - are there extra quote marks in this message?"
            ).format(name)
        )

    def get_card_members(self, card):
        """Return an array of Trello.Member objects of this card

        :param card:
        """
        return [self.get_member(member_id) for member_id in card.member_id]

    @lru_cache()
    def get_member(self, member_id):
        """Get a member. We only use our own function so that we can cache calls

        :param member_id:
        """
        return self.client.get_member(member_id)

    def first(self, iterable, condition):
        """Iterates an iterable and returns the first item that meets a condition or None

        :param iterable: An iterable to fetch the first itemm that meets condition
        :param condition: The condition to evaluate per item
        """
        return next((i for i in iterable if condition(i)), None)

    def get_done_cards(self):
        """Get every card from the done list"""
        return self.done.list_cards()

    def prep_card(self, card):
        """Take the card and add arrays of all member initials, full_names and usernames for use in templates

        :param card: a card to modify with extra information
        """

        card.members = self.get_card_members(card)
        card.members_initials = ""
        card.members_full_names = ""
        card.members_usernames = ""
        if len(card.members):
            card.members_initials = [member.initials for member in card.members]
            card.members_full_names = [member.full_name for member in card.members]
            card.members_usernames = [member.username for member in card.members]
        return card

    def summarize_these(self, cards, template, prep_function):
        """Run a list of cards through a template and return those joined by newlines
        The template can reference any part of a Trello.card as well as 3 handy arrays
        - members_initials
        - members_full_names
        - members_usernames
        These will either have an empty string or an array of strings that show up nicely
        in string.format

        :param cards: Card objects to summarize
        :param template: A template for each card. We pass the full card to format
        :param prep_function: A function that will add make the card more friendly to format
        """
        summary = "\n".join(
            [self.summarize_this(card, template, prep_function) for card in cards]
        )
        return summary

    def summarize_this(self, card, template, prep_function):
        """Summarize a card by passing it to a template after prepping it with values from a prep_function

        :param card: a Card to summarize
        :param template: a string template. We'll call format and pass in a prepped Card
        :param prep_function: use this to add extra information to the card 
        """
        card = prep_function(self, card)
        summary = template.format(card=card)
        return summary

    def create_release_card(self, cards, release_template, card_summary_template):
        """Returns a new release card, with a title from template and description based on a summary of the cards

        :param cards: Cards in this release
        :param release_template: A format string for release card name that we pass in date and length of cards
        :param card_summary_template: A string we format with per each card
        """
        release_card_name = release_template.format(date=date.today(), count=len(cards))
        # turn list of names of cards into a summary
        summary = self.summarize_these(
            cards, template=card_summary_template, prep_function=self.prep_card
        )
        logger.info(f"{summary}")
        release_card = self.releases.add_card(release_card_name, summary)
        return release_card

    def add_comment_to_release(
        self,
        release_card,
        card,
        comment_format="{card.name}\n{card.url}\n{card.description}",
    ):
        """add_comment_to_release

        :param release_card: A card to comment on
        :param card: A card to summarize in a comment
        :param comment_format: The template, passed in the card.
        """
        comment_text = comment_format.format(card=card)
        release_card.comment(comment_text)
