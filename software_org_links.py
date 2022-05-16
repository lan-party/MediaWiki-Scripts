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

# Collect website links from all software pages
software_links = {}
print("Collecting Software Sites - "+str(len(software)))
for a in range(0, len(software)):
    if a % 100 == 0 and a != 0:
        print(str(round((a/len(software))*100))+"%")
    try:
        link = str(requests.get("https://bciwiki.org"+software[a]).content)
        link = link.split('"external text" href="')[2]
        link = link.split('"')[0]
        if "sites.google.com" not in link:
            if '//' in link:
                link = link.split('//')[1]
            if '/' in link:
                link = link.split('/')[0]
            if link in software_links:
                software_links[link] += [software[a]]
            else:
                software_links[link] = [software[a]]
    except Exception:
        pass
print(software_links)

# Link to org pages from software/dev tools with matching domain name
for software_link in software_links:
    if software_link in org_links:
        for a in range(0, len(software_links[software_link])):
            org_list = "\n==Organizations==\n"
            for b in range(0, len(org_links[software_link])):
                org_name = org_links[software_link][b].split("/")[2]
                org_list += "*[["+org_name+"|"+org_name.replace("_", " ")+"]]\n"
            try:
                resp = requests.get("https://bciwiki.org/index.php?title="+software_links[software_link][a].split("/")[2]+"&action=edit").text
                if 'wpTextbox1">' in resp:
                    resp = resp.split('wpTextbox1">')[1]
                    resp = resp.split('</textarea>')[0]
                    resp = resp.replace("\\n", "\n")
                    resp = resp.replace("\\", "")
                    if "==Organizations==" not in resp and "[[Category:Software]]" not in resp:
                        newtext = resp.replace("==Links==", org_list+"==Links==")
                        print(software_links[software_link][a].split("/")[2])
                        print(newtext)
                        resp = str(requests.post("https://bciwiki.org/index.php?title="+software_links[software_link][a].split("/")[2]+"&action=submit", params={
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
                        print(software_links[software_link][a].split("/")[2])
                        print(org_list)
                        os.system('cmd /c "echo '+org_list.replace("\n", "&echo ")+'" | clip')
                        os.system("start https://bciwiki.org"+software_links[software_link][a])
                        input()
            except Exception:
                pass

# Link to software/dev tools from org pages with matching domain name
for org_link in org_links:
    if org_link in software_links:
        for a in range(0, len(org_links[org_link])):
            software_list = "\n==Software==\n"
            for b in range(0, len(software_links[org_link])):
                software_name = software_links[org_link][b].split("/")[2]
                software_list += "*[["+software_name+"|"+software_name.replace("_", " ")+"]]\n"
            try:
                resp = requests.get("https://bciwiki.org/index.php?title="+org_links[org_link][a].split("/")[2]+"&action=edit").text
                if 'wpTextbox1">' in resp:
                    resp = resp.split('wpTextbox1">')[1]
                    resp = resp.split('</textarea>')[0]
                    resp = resp.replace("\\n", "\n")
                    resp = resp.replace("\\", "")
                    if "==Software==" not in resp and "[[Category:Organizations]]" not in resp:
                        newtext = resp.replace("==Links==", software_list+"==Links==")
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
                    if "==Software==" not in resp:
                        print(org_links[org_link][a].split("/")[2])
                        print(software_list)
                        os.system('cmd /c "echo '+software_list.replace("\n", "&echo ")+'" | clip')
                        os.system("start https://bciwiki.org"+org_links[org_link][a])
                        input()
            except Exception:
                pass
