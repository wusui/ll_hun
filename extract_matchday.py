import requests
from html.parser import HTMLParser

class DayParse(HTMLParser):
    # pylint: disable=W0223
    def __init__(self):
        HTMLParser.__init__(self)
        self.results = {'data': [], 'plist': [], 'sinfo': []}
        self.count = 0
        self.tcount = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            for apt in attrs:
                if apt[0] == 'class':
                    if apt[1].startswith('ind-Yes'):
                        self.results['data'].append('Y')
                    if apt[1].startswith('ind-No'):
                        self.results['data'].append('N')
        if tag == 'a':
            if self.count < 4:
                for apt in attrs:
                    if apt[0] == 'href':
                        if apt[1].startswith('/profiles.php?'):
                            self.results['plist'].append(apt[1].split('?')[1])
                            self.count +=  1
                        if apt[1].startswith('/profiles/'):
                            self.results['plist'].append(apt[1].split('/')[2])
                            self.count += 1

    def handle_data(self, data):
        if self.tcount < 4:
            if len(data) == 4:
                if data[1]== '(':
                    if data[3] == ')':
                        self.results['sinfo'].append(data)
                        self.tcount += 1

def format_matchday(info):
    retval = {}
    for plyr in range(0,2):
        noval = 'N'
        findx = plyr
        if len(info['sinfo']) == 4:
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
    ndata = requests.get(htmladdr)
    parser = DayParse()
    parser.feed(ndata.text)
    return format_matchday(parser.results)

if __name__ == "__main__":
    tests = ['match.php?id=2156538',
             'match.php?id=2104667',
             'll49/questions/43606601.shtml',
             'll45/questions/43646106.shtml']
    for entry in tests:
        htmladdr = 'https://learnedleague.com/%s' % entry
        print(extract_matchday(htmladdr));