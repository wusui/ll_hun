#!/usr/bin/python3
"""
Extract all answers from a player
"""
from html.parser import HTMLParser
from collections import OrderedDict
import yaml
import os

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
                            
def eprint(estring):
    """
    Embellish an error message
    """
    print('************** ERROR **************')
    print(estring)
    print('***********************************')

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
        eprint('userinfo.ini file may be incorrect')
    parser.feed(ndata.text)
    return parser.result

def check_answers(answers):
    """
    Display answers
    """
    print(answers)
    if len(answers) != 150:
        eprint('The number of answers appears to be incorrect')

def get_data_for_person(name):
    """
    Input:
         Name-- Learned league name

    Output:
        Dictionary of 150 character strings of answers, indexed by season number.
    """
    sdata = get_session()
    session = sdata[0]
    active_season = sdata[1]
    verbose = sdata[2]
    odata = extract_person(name, session)
    session.close()
    user_info = {}
    prev_no = 25
    prev_season = 0
    season = 0
    count = 0
    odata1 = OrderedDict(sorted(odata.items()))
    for parts in odata1:
        indx = parts
        value = odata1[parts]
        mday = indx % 100
        if mday == 1:
            prev_season = season
            if season != 0:
                check_answers(user_info[season])
            season = indx // 100
            print("Collecting data for Season %s" % season)
            if prev_no != 25:
                if prev_season != active_season:
                    eprint('season error for entry %i' % indx)
            user_info[season] = ''
        else:
            if season != indx // 100:
                eprint('seasons out of order for entry %i' % indx)
            if prev_no + 1 != mday:
                eprint('match day order error for entry %i' % indx)
        prev_no = mday
        count += 1
        if verbose:
            print(str(count)+": "+str(indx)+' '+value)
        user_info[season] += extract_matchday('%s%s' % (HEAD, value))[name]
    check_answers(user_info[season])
    return user_info

def get_data_for(name, dirv):
    """
    Collect a person's answer data

    Input:
        name: person
    """
    idv = name.lower()
    data = get_data_for_person(idv)
    filename = os.path.join(dirv, idv+".yaml")
    out_info = yaml.dump(data)
    with open(filename, 'w') as ofile:
        ofile.write(out_info)

if __name__ == "__main__":
    get_data_for('shelburnem', 'people')
