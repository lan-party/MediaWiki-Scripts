import requests
import math

# Get all page links from category page
def getLinks(r):
    orgs = []
    sections = r.split("</h3>")[1:-8]
    for section in sections:
        links = section.split('href="')[1:]
        for link in links:
            if "index.php/" in link:
                orgs += [link.split('"')[0]]
    return orgs

# Get all organization links
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

print("Organization pages: "+str(len(organizations)))


# Find and report any organizations with broken website
for org in organizations:
    link = str(requests.get("https://bciwiki.org"+org).content)
    link = link.split('"external text" href="')[1]
    link = link.split('"')[0]
    try:
        resp = requests.get(link)
        if resp.status_code != 200:
            print(org)
        else:
            if "404" in resp and "wix" in resp and "Error" in resp:
                print(org)
    except Exception:
        pass
