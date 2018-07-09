#!/usr/bin/python3
from gen_hun_number import get_all_tables
import display_constants

import os

def write_entry(fd, text):
    """
    Write text info file fd, with the surronding format of a table cell
    """
    fd.write("<td class=center>%s</td>" % text)

def make_html(short_name, long_name):
    """
    This assumes that the data has been populated into a directory named short_name
    Write short_name/short_name.html, a web page displaying Hun values for a rundle
    Short_name is the short name of the rundle used by Learned League
    Long_name is used to title the page output.
    """
    fname = os.path.join("%s" % short_name, "%s.html" % short_name)
    data = get_all_tables(short_name)
    with open(fname, 'w') as out_file:
        out_file.write(display_constants.DISPLAY_HEADER % long_name)
        out_file.write(display_constants.CSS_SECTION)
        out_file.write(display_constants.DISPLAY_TITLE % long_name)
        for name in data[0]:
            out_file.write(display_constants.TABLE_HEAD % name)
            for info in data[1][name]:
                print(info)
                out_file.write('<tr>')
                write_entry(out_file, info[0])
                oval = info[1][1] + .00005
                write_entry(out_file, str(oval)[0:6])
                write_entry(out_file, str(info[1][0]))
                out_file.write('</tr>')
            out_file.write('</table>')
        out_file.write('</body></html>')

if __name__ == "__main__":
    #
    # Use O'Brien's Pub as a guinea pig
    #
    make_html("B_Pacific", "Season 77, B Pacific")
