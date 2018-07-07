#!/usr/bin/python3
"""
Extract all answers from a player
"""
from html.parser import HTMLParser

from extract_matchday import extract_matchday
from get_session import get_session
from get_session import HEAD

class PersonParse(HTMLParser):
    """
    Html parser for the games played profile of a user.
    """
    # pylint: disable=W0223
    def __init__(self):
        """
        Initialize the following:
            mday -- match day number
            season -- season number
            result -- dictionary of matches played
        """
        HTMLParser.__init__(self)
        self.mday = 0
        self.season = 0
        self.result = {}
    
    def handle_starttag(self, tag, attrs):
        """
        Scan for match data.  The first section handles newer (after LL51)
        match day information formats.
        """
        if tag == 'a':
            for apt in attrs:
                if apt[0] == 'href':
                    if apt[1].startswith('/match.php?'):
                        info = apt[1].split('?')[1]
                        if info.startswith('id='): 
                            self.result[self.season*100 + self.mday] = apt[1]
                        else:
                            parts = info.split('&')
                            self.season = int(parts[0])
                            self.mday = int(parts[1])
                    if '/questions/' in apt[1]:
                        qparts = apt[1].split('/')
                        self.season =  int(qparts[1][2:])
                        if not qparts[3].startswith('mdr'):
                            if qparts[3].startswith('md'):
                                self.mday = int(qparts[3][2:4])
                            if qparts[3][0].isdigit():
                                self.result[self.season*100 + self.mday] = apt[1]
                            
def extract_person(name, ses):
    """
    Input:
        name -- user name
        ses -- Session, needed to keep logged in
        
    Returns:
        dictionary of matchday url parts indexed by season and matchday
    """
    urlp = "%sprofiles/previous.php?%s" % (HEAD, name.lower())
    ndata = ses.get(urlp)
    parser = PersonParse()
    if ndata.text.startswith('Must be logged in'):
        print('userinfo.ini file may be incorrect')
    parser.feed(ndata.text)
    return parser.result

if __name__ == "__main__":
    #
    # View the match info filenames one by one.
    #
    s = get_session()
    odata = extract_person('muellerp', s)
    s.close()
    count = 0
    for i in odata:
        count += 1
        print(str(count)+": "+str(i)+' '+odata[i])
        print(extract_matchday('%s%s' % (HEAD, odata[i])))