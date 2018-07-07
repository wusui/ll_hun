#!/usr/bin/python3
"""
Extract data from a matchday
"""
import requests
from html.parser import HTMLParser
from get_session import HEAD

DATA_LIMIT = 4
class DayParse(HTMLParser):
    # pylint: disable=W0223
    """
    Html parser for match day web pages
    """
    def __init__(self):
        """
        Initialize the following:
        results -- information we want to display -- read by format_matchday
        count -- counter of possible player names
        tcount -- counter of possible scores
        """
        HTMLParser.__init__(self)
        self.results = {'data': [], 'plist': [], 'sinfo': []}
        self.count = 0
        self.tcount = 0

    def handle_starttag(self, tag, attrs):
        """
        Check for Y or N answers.
        Check for player's names.
        """
        if tag == 'td':
            for apt in attrs:
                if apt[0] == 'class':
                    if apt[1].startswith('ind-Yes'):
                        self.results['data'].append('Y')
                    if apt[1].startswith('ind-No'):
                        self.results['data'].append('N')
        if tag == 'a':
            if self.count < DATA_LIMIT:
                for apt in attrs:
                    if apt[0] == 'href':
                        if apt[1].startswith('/profiles.php?'):
                            self.results['plist'].append(apt[1].split('?')[1])
                            self.count +=  1
                        if apt[1].startswith('/profiles/'):
                            self.results['plist'].append(apt[1].split('/')[2])
                            self.count += 1

    def handle_data(self, data):
        """
        Check for scores listed.
        """
        if self.tcount < DATA_LIMIT:
            if len(data) == DATA_LIMIT:
                if data[1]== '(':
                    if data[3] == ')':
                        self.results['sinfo'].append(data)
                        self.tcount += 1

def format_matchday(info):
    """
    Input:
        info -- dictionary with three elements:
                data -- list of Y, N, or _ (forfeit) answers in the order they appear on
                        the page that was parsed.
                plist -- list of player names appearing on the page (in order of
                         appearance)
                sinfo -- list of scores shown (in order of appearance)
    Returns:
        dictionary indexed by player names.  Each entry is that player's 6 answers.
    """
    retval = {}
    for plyr in range(0,2):
        noval = 'N'
        findx = plyr
        if len(info['sinfo']) == DATA_LIMIT:
            findx *= 2
        if info['sinfo'][findx] == '0(F)':
            noval = '_'
        qstr = ''
        for qnum in range(0,6):
            if info['data'][qnum*2 + plyr] == 'N':
                qstr += noval
            else:
                qstr += 'Y'
        pname = info['plist'][plyr*2]
        if pname.endswith('.shtml'):
            pname = pname[0:len(pname)-len('.shtml')]
        retval[pname] = qstr
    return retval

def extract_matchday(htmladdr):
    """
    Input:
         htmladdr -- html address of matchday to be read.
    Returns:
        dictionary indexed by player where each entry a six character long
        string representing the answers that person gave on this matchday
    """
    ndata = requests.get(htmladdr)
    parser = DayParse()
    parser.feed(ndata.text)
    return format_matchday(parser.results)

if __name__ == "__main__":
    #
    # Test new matchday without forfeit, new matchday with forfeit,
    # old matchday withoug forfeit, and old matchday wit forfeit.
    #
    # old matchday format is LL51 and earlier.
    #
    tests = ['match.php?id=2156538',
             'match.php?id=2104667',
             'll49/questions/43606601.shtml',
             'll45/questions/43646106.shtml']
    for entry in tests:
        htmladdr = '%s%s' % (HEAD, entry)
        print(extract_matchday(htmladdr))
