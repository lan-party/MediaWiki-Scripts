import requests
import time
from lxml import html
import os

# Collect links from goodreads by search term
search_terms = ["neuromonitoring", "brain computer interface", "brain machine interface", "electroencephalography", "neuroimaging",  "neurostimulation", "neuromodulation", "positron emission tomography",
                "magnetic resonance imaging", "near-infrared spectroscopy", "optogenetics", "transcranial magnetic stimulation", "vagus nerve stimulation",
                "transcranial direct current stimulation", "transcranial alternating current stimulation", "electrical brain stimulation", "deep brain stimulation"]

links = []
for c in range(0, len(search_terms)):
    resp = requests.get("https://www.goodreads.com/search?q="+search_terms[c].replace(" ", "+"))
    pagecount = 2
    if '</a> <a class="next_page"' in str(resp.content):
        pagecount = str(resp.content).split('</a> <a class="next_page"')[0]
        pagecount = int(pagecount.split(">")[len(pagecount.split(">"))-1])
    for b in range(1, pagecount):
        if b > 1:
            resp = requests.get("https://www.goodreads.com/search?q="+search_terms[c].replace(" ", "+")+"&page="+str(b))
        if '<a class="bookTitle" itemprop="url" href="' in str(resp.content):
            sections = str(resp.content).split('<a class="bookTitle" itemprop="url" href="')
            for a in range(1, len(sections)):
                link = sections[a].split("?")[0]
                if link not in links:
                    links += [link]
        print("Search term: "+search_terms[c]+" - page "+str(b)+" - "+str(len(links))+" links")
        time.sleep(3)

input(links)
gr = open("goodreads.txt", "a")
for a in range(0, len(links)):
    gr.write(links[a])
gr.close()

links = open("goodreads.txt", "r").read().splitlines()

# Collect book info: title, authors, isbn, description
for a in range(1500, len(links)):
    resp = requests.get("https://www.goodreads.com"+links[a])

    description = ''
    if str(resp.content).count('freeText') > 1:
        description = str(resp.content).split('freeText')[2]
        description = description[description.find(">")+1:]
        description = description.split("</span>")[0]
        description = description.replace("<br />", "\n")
        description = description.replace("\\'", "'")
        description = html.fromstring(description)
        description = description.text_content().strip()

    bookid = ''
    if '<div class="infoBoxRowItem">\\n                  ' in str(resp.content):
        bookid = str(resp.content).split('<div class="infoBoxRowItem">\\n                  ')[1]
        bookid = bookid.split('\\n                      <span class="greyText">')[0]
    elif "<div class=\"infoBoxRowItem\" itemprop='isbn'>" in str(resp.content):
        bookid = str(resp.content).split("<div class=\"infoBoxRowItem\" itemprop='isbn'>")[1]
        bookid = bookid.split('</div>')[0]
    else:
        continue

    sections = str(resp.content).split('<span itemprop="name">')
    authors = ""
    for b in range(1, len(sections)):
        if len(sections) > 2:
            if b == 1:
                authors += sections[b].split("<")[0]
            elif b < len(sections):
                authors += ", "+sections[b].split("<")[0]
            else:
                authors += ", and "+sections[b].split("<")[0]
        else:
            authors = sections[b].split("<")[0]
    
    title = str(resp.content).split('<h1 id="bookTitle" class="gr-h1 gr-h1--serif" itemprop="name">\\n      ')
    title = title[1].split('\\n</h1>')[0]

    print("===============================================")
    print("https://www.goodreads.com"+links[a])
    print(description)
    print(bookid)
    print(authors)
    input(title)

    # Format text for new wiki page
    pagetext = "[[Category:Books]]\n"
    if ", and " in authors:
        pagetext += "'''Authors: ''' "+authors+"\n\n"
    else:
        pagetext += "'''Author: ''' "+authors+"\n\n"
    pagetext += "'''ISBN/ASIN: ''' "+bookid+"\n\n"
    pagetext += description+"\n"
    pagetext += "==Links==\n"
    pagetext += "[https://www.goodreads.com"+links[a]+" Goodreads]\n"
    pagetext += "[ Amazon]" # Search ISBN or title on Amazon during page creation
    
    # Copy text to clipboard and open a new wiki page
    os.system('cmd /c "echo '+pagetext.replace("\n", "&echo.")+'" | clip')
    os.system("start https://bciwiki.org/index.php/"+title.replace(" ", "%20").replace("&", "%26"))
    input("=============== Row "+str(a)+" : "+str(round((a/len(links))*100, 2))+"% complete ===============")

