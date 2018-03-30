"""Get a list of forks from github."""
import json
import pandas as pd
import requests

url = "https://api.github.com/repos/Design-Computing/code1161/forks"
r = requests.get(url + "?per_page=100")
theJson = json.loads(r.text)


def get_the_useful(j):
    """Extract the information I care about from a person's data."""
    login = j[u"owner"][u'login']
    url = j[u"clone_url"]
    name = j[u"name"]
    return {"login": login, "url": url, "name": name}


deets = [get_the_useful(j) for j in theJson]
print(len(deets))
df = pd.DataFrame(deets)
print("\n\nResults:\n", df)
df.to_csv("csv/github.csv", index=False, columns=["login", "url", "name"])
