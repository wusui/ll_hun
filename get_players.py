#!/usr/bin/python3
"""
Extract all players from a rundle
"""
from html.parser import HTMLParser
import os

from get_session import get_session
from get_session import HEAD
from extract_person import get_data_for

class RundleParse(HTMLParser):
    # pylint: disable=W0223
    def __init__(self):
        """
        self.result -- list of player names found on this page
        """
        HTMLParser.__init__(self)
        self.result = []
    def handle_starttag(self, tag, attrs):
        """
        Find name in profile string.
        """
        if tag == 'a':
            for apt in attrs:
                if apt[0] == 'href':
                    if apt[1].startswith('/profiles.php?'):
                        pname = apt[1].split('?')[1]
                        self.result.append(pname)

def get_players(season, rundle):
    """
    Input:
        season -- season number
        rundle -- rundle name
        
    Returns:
        list of player names in that rundle.
    """
    sdata = get_session()
    session = sdata[0]
    fname = "%sstandings.php?%d&%s" % (HEAD, season, rundle)
    ndata = session.get(fname)
    parser = RundleParse()
    parser.feed(ndata.text)
    return parser.result[1:]

def populate(season, rundle):
    """
    Input:
        season -- season number
        rundle -- rundle name

    Loop through player list and save data.
    """
    out_str = get_players(season, rundle)
    os.mkdir(rundle)
    for pname in out_str:
        print('Extracting data for: %s' % pname)
        get_data_for(pname, rundle)
        
if __name__ == "__main__":
    #
    # Use O'Brien's Pub as a guinea pig
    #
    populate(77, "B_Pacific")
