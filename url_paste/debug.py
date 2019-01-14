import fileinput
import json

output = ''
for line in fileinput.input():
    output += line

items = json.loads(output)["items"]
print([x["arg"] for x in items if "RTF" in x["title"]][0])
