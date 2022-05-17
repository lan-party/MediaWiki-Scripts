import requests
import math
import os

# Session and wpEditToken are updated regularly by MediaWiki
# Retrieve from header and POST parameters sent by the browser on a save page request
sessionid = "***"
edittoken = "***"
wikitoken = "***"

# Get links from mediawiki category page content
def getLinks(r):
    orgs = []
    sections = r.split("</h3>")[1:-8]
    for section in sections:
        links = section.split('href="')[1:]
        for link in links:
            if "index.php/" in link:
                orgs += [link.split('"')[0]]
    return orgs

# Collect software pages
resp = str(requests.get("https://bciwiki.org/index.php/Category:Software").content)
software = []

software += getLinks(resp)

outof = resp.split("out of ")[1]
outof = float(outof.split(" ")[0])
pagecount = outof/200
pagecount = math.ceil(pagecount)

nextpage = resp.split(') (<a href="')[1]
nextpage = nextpage.split('"')[0]
nextpage = nextpage.replace("amp;", "")
nextpage = nextpage.replace("amp%", "")
while pagecount > 1:
    resp = str(requests.get("https://bciwiki.org"+nextpage).content)
    software += getLinks(resp)
    if ') (<a href="' in resp:
        nextpage = resp.split(') (<a href="')[1]
        nextpage = nextpage.split('"')[0]
        nextpage = nextpage.replace("amp;", "")
        nextpage = nextpage.replace("amp%", "")
    pagecount -= 1
print("Software List Collected")

# Add categories to software pages
for a in range(0, len(software)):
    if a % 25 == 0:
        print(a)
    name = software[a].split("/")[2]
    resp = requests.get("https://bciwiki.org/index.php?title="+name.replace(" ", "_")+"&action=edit").text
    if 'wpTextbox1">' in resp:
        resp = resp.split('wpTextbox1">')[1]
        resp = resp.split('</textarea>')[0]
        resp = resp.replace("\\n", "\n")
        newtext = resp
        if "play.google.com" in resp and "Category:Play_Store_Apps" not in resp:
            newtext = "[[Category:Play_Store_Apps]]\n"+newtext
        if "apps.apple.com" in resp and "Category:App_Store_Apps" not in resp:
            newtext = "[[Category:App_Store_Apps]]\n"+newtext
        if "GitHub]" in resp and "Category:GitHub_Repos" not in resp:
            newtext = "[[Category:GitHub_Repos]]\n"+newtext

        requests.post("https://bciwiki.org/index.php?title="+name.replace(" ", "_")+"&action=submit", params={
            "wpUnicodeCheck": open("unicode.txt", mode="r", encoding="utf-8").read(),
            "wpSave": "Save changes",
            "format": "text/x-wiki",
            "model": "wikitext",
            "editingStatsId": "",
            "wpStarttime": "",
            "wpEdittime": "",
            "wpTextbox1": newtext,
            "wpEditToken": edittoken,
            "wpWatchthis": "",
            "wpUltimateParam": "1",
            "mode": "text"}, cookies={
                        "ls_smartpush": "1",
                        "mw_installer_session": "",
                        "u216253868_bciwiki_session": sessionid,
                        "u216253868_bciwikiToken": wikitoken,
                        "u216253868_bciwikiUserID": "1",
                        "u216253868_bciwikiUserName": "Landonodnal",
                        "VEE": "wikitext",
                        "wikiEditor-0-toolbar-section": "advanced"
                }, headers={'Content-type': 'text/html; charset=utf-8'})
    else:
        print(name)


# Collect dev tool pages
resp = str(requests.get("https://bciwiki.org/index.php/Category:Developer_Tools").content)
devtools = getLinks(resp)
print("Developer Tools List Collected")

# Add categories to dev tool pages
for a in range(0, len(devtools)):
    if a % 25 == 0:
        print(a)

    name = devtools[a].split("/")[2]
    resp = requests.get("https://bciwiki.org/index.php?title="+name.replace(" ", "_")+"&action=edit").text
    if 'wpTextbox1">' in resp:
        resp = resp.split('wpTextbox1">')[1]
        resp = resp.split('</textarea>')[0]
        resp = resp.replace("\\n", "\n")
        newtext = resp
        if "play.google.com" in resp and "Category:Play_Store_Apps" not in resp:
            newtext = "[[Category:Play_Store_Apps]]\n"+newtext
        if "apps.apple.com" in resp and "Category:App_Store_Apps" not in resp:
            newtext = "[[Category:App_Store_Apps]]\n"+newtext
        if "GitHub]" in resp and "Category:GitHub_Repos" not in resp:
            newtext = "[[Category:GitHub_Repos]]\n"+newtext

        requests.post("https://bciwiki.org/index.php?title="+name.replace(" ", "_")+"&action=submit", params={
            "wpUnicodeCheck": open("unicode.txt", mode="r", encoding="utf-8").read(),
            "wpSave": "Save changes",
            "format": "text/x-wiki",
            "model": "wikitext",
            "editingStatsId": "",
            "wpStarttime": "",
            "wpEdittime": "",
            "wpTextbox1": newtext,
            "wpEditToken": edittoken,
            "wpWatchthis": "",
            "wpUltimateParam": "1",
            "mode": "text"}, cookies={
                        "ls_smartpush": "1",
                        "mw_installer_session": "",
                        "u216253868_bciwiki_session": sessionid,
                        "u216253868_bciwikiToken": wikitokenn,
                        "u216253868_bciwikiUserID": "1",
                        "u216253868_bciwikiUserName": "Landonodnal",
                        "VEE": "wikitext",
                        "wikiEditor-0-toolbar-section": "advanced"
                }, headers={'Content-type': 'text/html; charset=utf-8'})
    else:
        print(name)
