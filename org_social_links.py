import requests
import math
import os


# Session and wpEditToken are updated regularly by MediaWiki
# Retrieve from header and POST parameters sent by the browser on a save page request
session = "***"
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

# Create link to add to page text
def getSocialAddition(link, dork, ignorelist, linktitle):
    socialadd = ""
    try:
        resp = str(requests.get(link).content)
        if dork in resp:
            resp = resp.split(dork)[1]
            if '"' in resp:
                if "'" in resp:
                    if resp.find('"') < resp.find("'"):
                        resp = resp.split('"')[0]
                    else:
                        resp = resp.split("'")[0]
                else:
                    resp = resp.split('"')[0]
            else:
                resp = resp.split("'")[0]
            ignore = False
            for ignoreitem in ignorelist:
                if ignoreitem in resp:
                    ignore = True
            if not ignore:
                socialadd = "[https://"+dork+resp+" "+linktitle+"]"
    except Exception:
        pass
    return socialadd

# Collect list of org links
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


# Find social links and add to organization pages
intext = []
print(len(organizations))
for a in range(0, len(organizations)):
    link = str(requests.get("https://bciwiki.org"+organizations[a]).content)
    link = link.split('"external text" href="')[2]
    link = link.split('"')[0]
    if a % 25 == 0:
        print(a)

    twitteradd = getSocialAddition(link, "twitter.com/", ["Tweets by ", "http", " ", "status/", "share", "squarespace", ".js"], "Twitter")
    fbadd = getSocialAddition(link, "facebook.com/", ["/fbml", "http", " ", "plugin", "tr?", "squarespace"], "Facebook")
    igadd = getSocialAddition(link, "instagram.com/", ["http", " ", "squarespace"], "Instagram")
    ytadd = getSocialAddition(link, "youtube.com/", ["http", " ", "watch?v=", "embed/", "squarespace", "iframe_api"], "YouTube")
    ghadd = getSocialAddition(link, "github.com/", ["http", " ", "squarespace"], "GitHub")

    if twitteradd != "" or fbadd != "" or igadd != "" or ytadd != "" or "linkedin.com/" in resp or "twitter.com/" in resp or "facebook.com/" in resp or "instagram.com/" in resp or "github.com/" in resp:
        # Include links and relevant categories in page text
        resp = requests.get("https://bciwiki.org/index.php?title="+organizations[a].split("/")[2]+"&action=edit").text
        if 'wpTextbox1">' in resp:
            resp = resp.split('wpTextbox1">')[1]
            resp = resp.split('</textarea>')[0]
            resp = resp.replace("\\n", "\n")
            resp = resp.replace("\\", "")
            newtext = resp
            if "twitter.com/" not in resp:
                newtext += twitteradd
            if "[[Category:Twitter Accounts]]" not in resp and "twitter.com/" in newtext:
                newtext = "[[Category:Twitter Accounts]]\n"+newtext
                print(organizations[a]+" - twitter category")
            if "facebook.com/" not in resp:
                newtext += fbadd
            if "[[Category:Facebook Pages]]" not in resp and "facebook.com/" in newtext:
                newtext = "[[Category:Facebook Pages]]\n"+newtext
                print(organizations[a]+" - facebook category")
            if "instagram.com/" not in resp:
                newtext += igadd
            if "[[Category:Instagram Pages]]" not in resp and "instagram.com/" in newtext:
                newtext = "[[Category:Instagram Pages]]\n"+newtext
                print(organizations[a]+" - instagram category")
            if "youtube.com/" not in resp:
                newtext += ytadd
            if "[[Category:YouTube Channels]]" not in resp and "youtube.com/" in newtext:
                newtext = "[[Category:YouTube Channels]]\n"+newtext
                print(organizations[a]+" - youtube category")
            if "github.com/" not in resp:
                newtext += ghadd
            if "[[Category:GitHub Accounts]]" not in resp and "github.com/" in newtext:
                newtext = "[[Category:GitHub Accounts]]\n"+newtext
                print(organizations[a]+" - github category")
            if "[[Category:LinkedIn Accounts]]" not in resp and "linkedin.com/" in newtext:
                newtext = "[[Category:LinkedIn Accounts]]\n"+newtext
                print(organizations[a]+" - linkedin category")

            # Update page text
            resp = str(requests.post("https://bciwiki.org/index.php?title="+organizations[a].split("/")[2]+"&action=submit", params={
                "wpUnicodeCheck": open("unicode.txt", mode="r", encoding="utf-8").read(),
                "wpSave": "Save changes",
                "format": "text/x-wiki",
                "model": "wikitext",
                "editingStatsId": "7f2242361389761f3b10bafae723dc66",
                "wpStarttime": "",
                "wpEdittime": "",
                "wpTextbox1": newtext,
                "wpEditToken": edittoken,
                "wpWatchthis": "",
                "wpUltimateParam": "1",
                "mode": "text"}, cookies={
                            "ls_smartpush": "1",
                            "mw_installer_session": "12a3a7a4b67dc73e0caf0771faa52610",
                            "u216253868_bciwiki_session": session,
                            "u216253868_bciwikiToken": wikitoken,
                            "u216253868_bciwikiUserID": "1",
                            "u216253868_bciwikiUserName": "Landonodnal",
                            "VEE": "wikitext",
                            "wikiEditor-0-toolbar-section": "advanced"
                    }, headers={'Content-type': 'text/html; charset=utf-8'}).content)
        else:
            print(organizations[a].split("/")[2])
