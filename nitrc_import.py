import requests
import os

# Search parameters for Magnetic Resonance software
mr_d = {"type_of_search": "group",
"offset": "0",
"removeterm": "",
"cat": "628",
"compare": "",
"q": "",
"offset": "0",
"q_within_results": "",
"search_explanation": "",
"rows": "1000",
"s": "relevancy",
"xrowsx": "20",
"s": "relevancy"}

# Search parameters for EEG software
eeg_d = {"type_of_search": "group",
"offset": "0",
"removeterm": "",
"cat": "629",
"compare": "",
"q": "",
"offset": "0",
"q_within_results": "",
"search_explanation": "",
"rows": "1000",
"s": "relevancy",
"xrowsx": "20",
"s": "relevancy"}

# Get search results from NITRC
mr_resp = str(requests.post("https://www.nitrc.org/search/", data=mr_d).content)
mr_list = mr_resp.split('panel-title">')[1:]
eeg_resp = str(requests.post("https://www.nitrc.org/search/", data=eeg_d).content)
eeg_list = eeg_resp.split('panel-title">')[1:]
combined_tools = eeg_list+mr_list
print(len(combined_tools))

save_state = 0 # Update manually with printed save-state

for a in range(save_state, len(combined_tools)):
    # filter by tools with the fa-code class
    if 'fa-code' in combined_tools[a]:
        # Extract tool page and name
        tool_url = combined_tools[a].split('href="')[1]
        tool_url = tool_url.split('"')[0]

        tool_name = combined_tools[a].split('">')[1]
        tool_name = tool_name.split('<')[0]
        tool_name = tool_name.replace("\\n", "")
        tool_name = tool_name.strip()
        
        # Extract description and website from tool page
        resp = str(requests.get("https://www.nitrc.org"+tool_url).content)
        description = ""
        if 'tool-description">' in resp:
            description = resp.split('tool-description">')[1]
            description = description.split("</div>")[2]
            description = description.replace("<br />", "\n")
            description = description.replace("\\n", "")
            description = description.replace("\\r", "")
            description = description.strip()
        website_url = ""
        if '>Visit Website' in resp:
            website_url = resp.split("\\'>Visit Website")[0]
            website_url = website_url.split("<a href=\\'")[-1]

        # Format new page text
        pagetext = "[[Category:Software]]\n"+description+"\n==Links==\n"
        if "github" in website_url:
            pagetext += "["+website_url+" GitHub]"
        else:
            pagetext += "["+website_url+" Website]"

        print("Save-State: "+str(a))
        print(pagetext)
        # Copy text to clipboard and open a new wiki page
        os.system('cmd /c "echo '+pagetext.replace("\n", "&echo ")+'" | clip')
        os.system("start "+website_url)
        os.system("start https://bciwiki.org/index.php/"+tool_name.replace(" ", "%20"))
        input("=============================================================")
