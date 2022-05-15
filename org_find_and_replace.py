import requests

savestate = 0

# Session and wpEditToken are updated regularly by MediaWiki
# Retrieve from header and POST parameters sent by the browser on a save page request
session = "***"
edittoken = "***"
wikitoken = "***"

# Collect organization list
resp = requests.get("https://bciwiki.org/index.php/Category:Organizations").text
resp = resp.split("</th></tr>")[1]
resp = resp.split("</tbody>")[0]
companies = resp.split("<tr>")
companynames = []
allcompanyinfo = [[]]
allcompanyindex = 0
for a in range(1, len(companies)):
    companyinfo = companies[a].split("<td>")
    for b in range(1, len(companyinfo)):
        if "<a" in companyinfo[b]:
            name = companyinfo[b].split('<a href="')[1]
            name = name.split('"')[0]
            name = "/".join(name.split("/")[2:])
            allcompanyinfo[allcompanyindex] += [name]
        else:
            info = companyinfo[b].split("\\n</td>")[0]
            allcompanyinfo[allcompanyindex] += [info]
        if b == 11:
            allcompanyindex += 1
            allcompanyinfo += [[]]
allcompanyinfo.pop()
print(len(allcompanyinfo))

for a in range(savestate, len(allcompanyinfo)):
    companyinfo = allcompanyinfo[a]
    if a % 25:
        print(a) # Print save state on every 25 orgs

    # Get current page text
    resp = requests.get("https://bciwiki.org/index.php?title="+companyinfo[0].replace(" ", "_")+"&action=edit").text
    resp = resp.split('wpTextbox1">')[1]
    resp = resp.split('</textarea>')[0]
    resp = resp.replace("\\n", "\n")

    # Find and replace substrings in page text
    resp = resp.replace("xe2x80x9c", "")
    resp = resp.replace("amp;", "")
    resp = resp.replace("gt;", "")

    # Update page content
    resp = str(requests.post("https://bciwiki.org/index.php?title="+companyinfo[0].replace(" ", "_")+"&action=submit", params={
        "wpUnicodeCheck": open("unicode.txt", mode="r", encoding="utf-8").read(),
        "wpSave": "Save changes",
        "format": "text/x-wiki",
        "model": "wikitext",
        "editingStatsId": "",
        "wpStarttime": "",
        "wpEdittime": "",
        "wpTextbox1": resp,
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
