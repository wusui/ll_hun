#!/usr/bin/python3
from load_info import load_info
"""
Generate Hun numbers
"""
class Hun_finder():
    """
    Object used to hold hun values while calculating and arranging them
    """
    def __init__(self, rundle):
        """
        Read all the data in.
        """
        self.plist = load_info(rundle)
        self.result = {}
        self.get_all_huns()

    def get_people(self):
        """
        Return a sorted list of players in the rundle.
        """
        return sorted(list(self.plist.keys()))

    def get_hun(self, player1, player2):
        """
        Calculate the hun value for the two players passsed.
        """
        same = 0
        diff = 0
        p1 = self.plist[player1]
        p2 = self.plist[player2]
        if len(p1) > len(p2):
            tmp = p2
            p2 = p1
            p1 = tmp
        for indx in p1.keys():
            if indx in p2.keys():
                for cno in range(0,150):
                    if p1[indx][cno:cno+1] == '_':
                        continue
                    if p2[indx][cno:cno+1] == '_':
                        continue
                    if p1[indx][cno:cno+1] == p2[indx][cno:cno+1]:
                        same += 1
                    else:
                        diff += 1
        tot = same + diff
        num = same/tot
        return (tot, num)

    def get_all_huns(self):
        """
        Stash hun values into result, indexed by a key derived from the names of
        the players who have this hun value.
        """
        for name1 in self.plist.keys():
            for name2 in self.plist.keys():
                if name1 < name2: 
                    nkey = name1+":"+name2
                    self.result[nkey] = self.get_hun(name1, name2)

    def show_result(self, person):
        """
        For an individual person, return a sorted list of the players with the
        highest hun numbers for that person.
        """
        myopps = {}
        for entry in self.result.keys():
            if person in entry:
                parts = entry.split(':')
                if person == parts[0]:
                    opp = parts[1]
                else:
                    opp = parts[0]
                myopps[opp] = self.result[entry]
        slist = list(myopps.items())
        return sorted(slist, key=lambda x: x[1][1], reverse=True)

def get_all_tables(rundle):
    """
    Given a rundle, return a tuple.
    The first element in the tuple is an alphabetically sorted list of rundle players.
    The second element is a dictionary indexed by players.
        Each element in that dictionary is a list of tuples sorted by hun number.
            Each tuple consists of the name of a player, and a tuple consisting of
            the number of questions answered in common and a hun number.
    """
    pval = Hun_finder(rundle)
    odata = {}
    for plyr in pval.get_people():
        odata[plyr] = pval.show_result(plyr)
    return (pval.get_people(), odata)

if __name__ == "__main__":
    #
    # Use O'Brien's Pub as a guinea pig
    #
    print(get_all_tables("OBriensIrishPub"))