import requests
import math

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

# Session and wpEditToken are updated regularly by MediaWiki
# Retrieve from header and POST parameters sent by the browser on a save page request
edittoken = "***"
session = "***"
wikitoken = "***"

# Collect org pages
resp = str(requests.get("https://bciwiki.org/index.php/Category:Organizations").content)
organizations = []

organizations += getLinks(resp)

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
    organizations += getLinks(resp)
    if ') (<a href="' in resp:
        nextpage = resp.split(') (<a href="')[1]
        nextpage = nextpage.split('"')[0]
        nextpage = nextpage.replace("amp;", "")
        nextpage = nextpage.replace("amp%", "")
    pagecount -= 1
print("Org List Collected")

# Collect dev tool pages
resp = str(requests.get("https://bciwiki.org/index.php/Category:Developer_Tools").content)
devtool = getLinks(resp)

print("Developer Tools List Collected")


# Collect website links from all org pages
org_links = {}
print("Collecting Org Sites - "+str(len(organizations)))
for a in range(0, len(organizations)):
    if a % 100 == 0 and a != 0:
        print(str(round((a/len(organizations))*100))+"%")
    try:
        link = str(requests.get("https://bciwiki.org"+organizations[a]).content)
        link = link.split('"external text" href="')[2]
        link = link.split('"')[0]
        if "sites.google.com" not in link:
            if '//' in link:
                link = link.split('//')[1]
            if '/' in link:
                link = link.split('/')[0]
            if link in org_links:
                org_links[link] += [organizations[a]]
            else:
                org_links[link] = [organizations[a]]
    except Exception:
        pass
print(org_links)

# Collect website links from all devtool pages
devtool_links = {}
print("Collecting Developer Tools Sites - "+str(len(devtool)))
for a in range(0, len(devtool)):
    if a % 100 == 0 and a != 0:
        print(str(round((a/len(devtool))*100))+"%")
    try:
        link = str(requests.get("https://bciwiki.org"+devtool[a]).content)
        link = link.split('"external text" href="')[2]
        link = link.split('"')[0]
        if "sites.google.com" not in link:
            if '//' in link:
                link = link.split('//')[1]
            if '/' in link:
                link = link.split('/')[0]
            if link in devtool_links:
                devtool_links[link] += [devtool[a]]
            else:
                devtool_links[link] = [devtool[a]]
    except Exception:
        pass
print(devtool_links)

# Link to org pages from devtools with matching domain name
for devtool_link in devtool_links:
    if devtool_link in org_links:
        for a in range(0, len(devtool_links[devtool_link])):
            org_list = "\n==Organizations==\n"
            for b in range(0, len(org_links[devtool_link])):
                org_name = org_links[devtool_link][b].split("/")[2]
                org_list += "*[["+org_name+"|"+org_name.replace("_", " ")+"]]\n"
            try:
                resp = requests.get("https://bciwiki.org/index.php?title="+devtool_links[devtool_link][a].split("/")[2]+"&action=edit").text
                if 'wpTextbox1">' in resp:
                    resp = resp.split('wpTextbox1">')[1]
                    resp = resp.split('</textarea>')[0]
                    resp = resp.replace("\\n", "\n")
                    resp = resp.replace("\\", "")
                    if "==Organizations==" not in resp and "[[Category:Developer_Tools]]" not in resp:
                        newtext = resp.replace("==Links==", org_list+"==Links==")
                        print(devtool_links[devtool_link][a].split("/")[2])
                        print(newtext)
                        resp = str(requests.post("https://bciwiki.org/index.php?title="+devtool_links[devtool_link][a].split("/")[2]+"&action=submit", params={
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
                    "u216253868_bciwiki_session": session,
                    "u216253868_bciwikiToken": wikitoken,
                    "u216253868_bciwikiUserID": "1",
                    "u216253868_bciwikiUserName": "Landonodnal",
                    "VEE": "wikitext",
                    "wikiEditor-0-toolbar-section": "advanced"
            }, headers={'Content-type': 'text/html; charset=utf-8'}).content)
                else:
                    if "==Organizations==" not in resp:
                        print(devtool_links[devtool_link][a].split("/")[2])
                        print(org_list)
                        os.system('cmd /c "echo '+org_list.replace("\n", "&echo ")+'" | clip')
                        os.system("start https://bciwiki.org"+devtool_links[devtool_link][a])
                        input()
            except Exception:
                pass

# Link to devtools from org pages with matching domain name
for org_link in org_links:
    if org_link in devtool_links:
        for a in range(0, len(org_links[org_link])):
            devtool_list = "\n==Developer Tools==\n"
            for b in range(0, len(devtool_links[org_link])):
                devtool_name = devtool_links[org_link][b].split("/")[2]
                devtool_list += "*[["+devtool_name+"|"+devtool_name.replace("_", " ")+"]]\n"
            try:
                resp = requests.get("https://bciwiki.org/index.php?title="+org_links[org_link][a].split("/")[2]+"&action=edit").text
                if 'wpTextbox1">' in resp:
                    resp = resp.split('wpTextbox1">')[1]
                    resp = resp.split('</textarea>')[0]
                    resp = resp.replace("\\n", "\n")
                    resp = resp.replace("\\", "")
                    if "==Developer Tools==" not in resp and "[[Category:Organizations]]" not in resp:
                        newtext = resp.replace("==Links==", devtool_list+"==Links==")
                        print(org_links[org_link][a].split("/")[2])
                        print(newtext)
                        resp = str(requests.post("https://bciwiki.org/index.php?title="+org_links[org_link][a].split("/")[2]+"&action=submit", params={
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
                    "u216253868_bciwiki_session": session,
                    "u216253868_bciwikiToken": wikitoken,
                    "u216253868_bciwikiUserID": "1",
                    "u216253868_bciwikiUserName": "Landonodnal",
                    "VEE": "wikitext",
                    "wikiEditor-0-toolbar-section": "advanced"
            }, headers={'Content-type': 'text/html; charset=utf-8'}).content)
                else:
                    if "==Developer Tools==" not in resp:
                        print(org_links[org_link][a].split("/")[2])
                        print(devtool_list)
                        os.system('cmd /c "echo '+devtool_list.replace("\n", "&echo ")+'" | clip')
                        os.system("start https://bciwiki.org"+org_links[org_link][a])
                        input()
            except Exception:
                pass
