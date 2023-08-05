# SPDX-License-Identifier: Apache-2.0
"""
A user agent string spoofer which can find common user agent strings, and
return a random string, based on up to date lists of widely used user agents.

This can be used be used to avoid tracking and fingerprinting, which aids
privacy and helps bypass anti-scraping measures and rate limiting.

User agent spoofing is also used to scrape the user agent lists themselves.

A Requests session subclass is provided which automatically uses a random user
agent on each connection.
"""

import json
from itertools import chain
from random import choice

from bs4 import BeautifulSoup
from requests import Session

# Dictionary with browser names as keys, and a list of aliases as the values
# Names are what are used as slugs on whatismybrowser.com
BROWSERS = {
    "chrome": ["chromium", "google-chrome"],
    "firefox": ["mozilla-firefox"],
    "safari": [],
    "internet-explorer": ["internetexplorer", "trident", "ie", "msie"],
    "edge": [],
    "opera": ["opr"],
    "vivaldi": [],
    "yandex-browser": ["yandex", "yabrowser"],
}
LANGS = ["*", "en", "en-US", "en-GB", "fr", "de", "es"]


def get_soup(s, url):
    """ Get a web page, try to parse it, and return its 'soup'. """
    res = s.get(url)
    if res.status_code != 200:
        return None
    try:
        soup = BeautifulSoup(res.text, "lxml")
    except ImportError:
        soup = BeautifulSoup(res.text, "html.parser")
    return soup


def get_ua_list1(s, ua):
    """
    Get a list of the latest User Agents by scraping whatismybrowser.com.
    Note that this may fail after repeated attempts due to IP blocking.
    """
    url = "https://www.whatismybrowser.com/guides/the-latest-user-agent/"
    for browser in BROWSERS:
        soup = get_soup(s, url + browser)
        if not soup:
            continue
        ua.setdefault(browser, set()).update(
            [tag.get_text() for tag in soup.tbody("span", class_="code")]
        )
    return ua


def get_ua_list2(s, ua):
    """
    Get a list of the most common user agents.
    Note that we use Google's cached version of the site due to Cloudflare's
    'anti-bot' page. This should be okay as the cache is updated often.
    """
    url = "https://techblog.willshouse.com/2012/01/03/most-common-user-agents/"
    cache = "https://webcache.googleusercontent.com/search?q=cache:FxxmQW9XrRcJ:"  # noqa
    soup = get_soup(s, cache + url)
    if not soup:
        return []
    raw_js = json.loads(soup("textarea", class_="get-the-list")[1].get_text())
    for js in raw_js:
        browser_name = js["system"].lower().split()[0]
        for browser, browser_aliases in BROWSERS.items():
            if browser == browser_name or browser_name in browser_aliases:
                ua.setdefault(browser, set()).add(js["useragent"])
                break
    return ua


GETTERS = [get_ua_list1, get_ua_list2]


class UserAgent:
    """
    The main entry point for the module: a class which provides lists of user
    agent strings and a property to get random user agents.
    """

    def __init__(self, session=None):
        self.dict = None
        self._all = None
        self.update(session)

    def update(self, session=None):
        """ Clear and rescrape the user agent list. """
        if not session:
            session = Session()
        self.dict = dict()
        for getter in GETTERS:
            self.dict = getter(session, self.dict)
        self._all = None

    @property
    def all(self):
        """ Return a single sorted list of all user agent strings. """
        if not self._all:
            self._all = sorted(chain.from_iterable(self.dict.values()))
        return self._all

    @property
    def random(self):
        """ Return a random user agent string. """
        return choice(self.all)

    def __getattr__(self, attr):
        for browser, aliases in BROWSERS.items():
            if attr == browser or attr in aliases:
                ua_set = self.dict.get(browser)
                if ua_set:
                    return choice(list(ua_set))
                raise AttributeError("No user agents found.")
        raise AttributeError("Unsupported browser: '{}'.".format(attr))


class SpoofSession(Session):
    """
    A Requests session subclass which uses a random user agent string on each
    connection. Also randomises other headers for extra anonymity.
    """

    def __init__(self):
        self.ua = UserAgent()
        super().__init__()

    def _new_headers(self):
        coin = [True, False]
        headers = {
            "Accept-Language": choice(LANGS),
            "User-Agent": self.ua.random,
        }
        flip = choice(coin)
        if flip:
            headers["DNT"] = "1"
        flip = choice([True, False])
        if flip:
            headers["Upgrade-Insecure-Requests"] = "1"
        self.headers.update(headers)
        return headers

    def request(self, method, url, **kwargs):
        """ HTTP Request """
        self._new_headers()
        self.cookies.clear()
        return super().request(method=method, url=url, **kwargs)
