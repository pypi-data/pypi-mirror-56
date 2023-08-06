#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from tweetpy.driver import Driver


class Twitter(Driver):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def login(self):
        self.load_url('https://twitter.com')

        username = self.get_element('[name="session[username_or_email]"]')
        self.input_element(username, self.username)

        password = self.get_element('[name="session[password]"]')
        self.input_element(password, self.password)

        submit = self.get_element('.submit.js-submit')
        self.click_element(submit)

        self.wait(2, 3)

    def tweet(self, content):
        self.load_url('https://twitter.com/home')

        self.wait(1, 3)

        # get the editor
        editor = self.get_element('[role="textbox"]')
        self.wait(1, 2)
        self.input_element(editor, ' ')
        self.input_element(editor, content)

        button = self.get_element('[data-testid="tweetButtonInline"]')
        self.click_element(button)

    def retweet_by_tag(self, tag, max=10):
        self.load_url(
            'https://twitter.com/search?q={}&src=typed_query&f=live'.format(
                tag
            )
        )
        self.wait(3, 4)
        tweets = self.get_elements('[data-testid="retweet"]')

        tweets = tweets[:10]
        print(len(tweets))

        for tweet in tweets:
            self.retweet(tweet)

    def retweet(self, element):
        self.click_element(element)
        self.wait(1, 2)

        confirm = self.get_element('[data-testid="retweetConfirm"]')
        self.click_element(confirm)
