#!/usr/bin/python3
DISPLAY_HEADER = '''<html>
<head>
    <title>
%s
    </title>
    <meta charset="UTF-8">
</head>'''

CSS_SECTION = '''<style type="text/css">
    body {
        font-family:sans-serif;
    }
    table.wfmt {
        border: 1px solid black;
    }
    h1 {
        text-align: center;
        margin-top: 40px;
    }
    th, td {
        border: 1px solid black;
        font-size: 15px;
        max-width: 100%;
        white-space: nowrap;
    }
    table.wfmt td.center
    {
        text-align: center;
    }
    table.wfmt td.left {
        text-align: left;
    }
    table.wfmt td.right {
        text-align: right;
    }
.wfmt { margin: 10px; auto;float: left; width: 20%}
</style>'''

DISPLAY_TITLE = '''<body>
<br>
<h1>HUN for -- %s</h1>
<br>
<br>'''

TABLE_HEAD = '''<table class=wfmt>
<tr><th class = center; colspan="4">%s</th></tr>
<tr><th>OPPOPNENT</th><th>HUN</th><th>Questions</th></tr>'''

if __name__ == "__main__":
    print(DISPLAY_HEADER % "O'Brien's Pub Quiz")
    print(CSS_SECTION)
    print(DISPLAY_TITLE % "O'Brien's Pub Quiz")
    print(TABLE_HEAD % "usuiw")
    print('</table>')
    print('</body></html>')
