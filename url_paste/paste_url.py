import sqlite3
import sys
import json
from os.path import expanduser
from contextlib import closing
from subprocess import Popen, PIPE

user_dir = expanduser("~")
dbname = '{}/Library/Application Support/Alfred 3/Databases/clipboard.alfdb'\
    .format(user_dir)

last_two = []
with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()
    get_last_two = '''SELECT item FROM clipboard ORDER BY ts DESC LIMIT 2'''
    for item in c.execute(get_last_two):
        last_two.append(item[0].encode('utf-8').strip())

if len(last_two) != 2:
    print('{"items": [{"title": "Error"}]}')
    sys.exit(0)

if last_two[0].startswith(b"http://") or last_two[0].startswith(b"https://"):
    url = last_two[0].decode('utf-8')
    title = last_two[1].decode('utf-8')
else:
    url = last_two[1].decode('utf-8')
    title = last_two[0].decode('utf-8')

markdown = u"[{title}]({url})".format(title=title, url=url)
html = u"<a href='{url}'>{title}</a>".format(url=url, title=title)
textutil = Popen(['textutil', '-stdin', '-format', 'html', '-convert', 'rtf', '-inputencoding', 'UTF-8', '-stdout'],
                 stdout=PIPE, stdin=PIPE, stderr=PIPE)
rtf = textutil.communicate(input=html.encode('utf-8'))[0]

output = {"items": [
    {
        "title": "Paste URL as RTF",
        "subtitle": rtf,
        "arg": rtf
    },
    {
        "title": "Paste URL as Markdown",
        "subtitle": markdown.encode('utf-8'),
        "arg": markdown.encode('utf-8')
    },
    {
        "title": "Paste URL as HTML",
        "subtitle": html.encode('utf-8'),
        "arg": html.encode('utf-8')
    }
]}

json_output = json.dumps(output, ensure_ascii=False)
print(json_output)
