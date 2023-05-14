import requests

# Start wiki session
print("Start wiki session")
S = requests.Session()
URL = "https://bciwiki.org/api.php"
# GET Request to fetch login token
PARAMS_0 = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}
R = S.get(url=URL, params=PARAMS_0)
DATA = R.json()
LOGIN_TOKEN = DATA['query']['tokens']['logintoken']
# POST Request to log in.
PARAMS_1 = {
    "action": "login",
    "lgname": "",
    "lgpassword": "",
    "lgtoken": LOGIN_TOKEN,
    "format": "json"
}
R = S.post(URL, data=PARAMS_1)
# GET request to fetch CSRF token
PARAMS_2 = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}
R = S.get(url=URL, params=PARAMS_2)
DATA = R.json()
CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

# alphabetize imaging and stimulation methods in company list
print("alphabetize imaging and stimulation methods in company list")
companies_page_content = requests.get("https://bciwiki.org/index.php?title=Category:Companies&action=edit").text
companies_page_content = companies_page_content[companies_page_content.find('name="wpTextbox1">')+18:companies_page_content.find("</textarea>")]

companies_table = companies_page_content.split("{|")[1]
companies_table = companies_table.split("|}")[0]
companies = companies_table.split("|-")
for company in companies:
    company_index = companies.index(company)
    if "\n|" in company:
        company = company.split("\n|")
        
        neurosensing_methods = company[10].split(", ")
        neurosensing_methods = ", ".join(sorted(neurosensing_methods))
        company[10] = neurosensing_methods
        
        neurostim_methods = company[11].split(", ")
        neurostim_methods = ", ".join(sorted(neurostim_methods))
        company[11] = neurostim_methods
        
        company = "\n|".join(company)
        
    companies[company_index] = company
companies_table = "|-".join(companies)

companies_page_content = companies_page_content.split("{|")
companies_page_content = companies_page_content[0] + "{|" + companies_table + "|}" + companies_page_content[1].split("|}")[1]
# POST request to edit a page
PARAMS_3 = {
    "action": "edit",
    "title": "Category:Companies",
    "token": CSRF_TOKEN,
    "format": "json",
    "text": companies_page_content
}
R = S.post(URL, data=PARAMS_3)
DATA = R.json()
print(DATA)

# alphabetize imaging and stimulation methods in software list
print("alphabetize imaging and stimulation methods in software list")
software_page_content = requests.get("https://bciwiki.org/index.php?title=Category:Software&action=edit").text
software_page_content = software_page_content[software_page_content.find('name="wpTextbox1">')+18:software_page_content.find("</textarea>")]

software_table = software_page_content.split("{|")[1]
software_table = software_table.split("|}")[0]
tools = software_table.split("|-")
for tool in tools:
    tool_index = tools.index(tool)
    if "\n|" in tool:
        tool = tool.split("\n|")
        
        neurosensing_methods = tool[3].split(", ")
        neurosensing_methods = ", ".join(sorted(neurosensing_methods))
        tool[3] = neurosensing_methods
        
        neurostim_methods = tool[4].split(", ")
        neurostim_methods = ", ".join(sorted(neurostim_methods))
        tool[4] = neurostim_methods
        
        tool = "\n|".join(tool)
        
    tools[tool_index] = tool
software_table = "|-".join(tools)

software_page_content = software_page_content.split("{|")
software_page_content = software_page_content[0]+ "{|" + software_table + "|}" + software_page_content[1].split("|}")[1]
# POST request to edit a page
PARAMS_3 = {
    "action": "edit",
    "title": "Category:Software",
    "token": CSRF_TOKEN,
    "format": "json",
    "text": software_page_content
}
R = S.post(URL, data=PARAMS_3)
DATA = R.json()
print(DATA)
