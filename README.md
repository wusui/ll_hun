# Find Hun Numbers for a given Rundle

This package creates an html file that displays Hun numbers for every player in that rundle vs. every other player in that rundle.

This package requires that python 3 is installed.

### userinfo.ini

Before any program can be run here, the file userinfo.ini needs to be created.  That file consists of:

```
[DEFAULT]
username = <username>
password = <password>
active_season = XX
verbose = no
```

username is the name of a Learned League user.  
password is the password for that Learned League user.  
active_season is the current season number, or next season if between seasons.  
verbose can be yes or no.  I recommend no.  

### Running the program

Start up python 3 and enter the following:

```
import make_html
make_html.complete(SEASON, SHORT_NAME, LONG_NAME)
```

where:
SEASON -- integer value of the season number  
SHORT_NAME -- short name of rundle used by Learned League.  Can be extracted as the data after question marks when following web pages.  
LONG_NAME -- header text on the rundle web page that is created.  

This runs for a while.  When finished, the html file containing the hun information is in short_name/short_name.html

For example, the following lines create an html page for season 77, B Pacific.

```
import make_html
make_html.complete(77, 'B_Pacific', "B Pacific Hun Values -- Season 77")
```
