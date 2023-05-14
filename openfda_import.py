import requests
import time

# API key
openfda_key = ""

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

# Loop through list of companies
companies = open("companies.txt", "r").read().splitlines()
for company in companies:
    print(company)
    # Get device listings from PMA endpoint (id, name, class, category)
    print("Get device listings from PMA endpoint (id, name, class, category)")
    skip = 0
    end_found = False
    pma_result_count = 0
    pma_results = []
    while not end_found:
        resp = requests.get("https://api.fda.gov/device/pma.json?search=applicant:"+company+"&limit=1000&skip="+str(skip)).json()
        try:
            if len(resp["error"]) > 0:
                end_found = True
        except Exception:
            try:
                for result in resp["results"]:
                    if company in result["applicant"]:
                        try:
                            pma_results.append([result["pma_number"], result["openfda"]["device_name"], result["openfda"]["device_class"], result["advisory_committee_description"]])
                            pma_result_count += 1
                        except Exception:
                            pass
            except Exception as e:
                print(resp)
                input(e)
            skip += 1000
            print(pma_result_count)
            # wait 1 second
            time.sleep(1)
    # Get device listings from PMN endpoints (id, name, class, category)
    print("Get device listings from PMN endpoint (id, name, class, category)")
    skip = 0
    end_found = False
    pmn_result_count = 0
    pmn_results = []
    while not end_found:
        resp = requests.get("https://api.fda.gov/device/510k.json?search=applicant:"+company+"&limit=1000&skip="+str(skip)).json()
        try:
            if len(resp["error"]) > 0:
                end_found = True
        except Exception:
            for result in resp["results"]:
                if company in result["applicant"]:
                    try:
                        pmn_results.append([result["k_number"], result["openfda"]["device_name"], result["openfda"]["device_class"], result["advisory_committee_description"]])
                        pmn_result_count += 1
                    except Exception:
                        pass
            skip += 1000
            print(pmn_result_count)
            # wait 1 second
            time.sleep(1)
    # if any results are returned
    if pma_result_count > 0 or pmn_result_count > 0:
        # Get current page contents from wiki
        company_page_content = requests.get("https://bciwiki.org/index.php?title="+company+"&action=edit").text
        company_page_content = company_page_content[company_page_content.find('name="wpTextbox1">')+18:company_page_content.find("</textarea>")]
        if "==FDA==" not in company_page_content:
            # Create formatted table and description text
            total_result_count = str(pma_result_count+pmn_result_count)
            new_content = "==FDA==\n"+company+" has "+total_result_count+" medical devices registered with the FDA. Here are some of them:\n"
            new_content += '{| class="wikitable" style="margin:auto"\n|+ Examples of FDA Approved Devices ([['+company.replace(" ", "_")+'_FDA_Devices | View List]])\n'
            new_content += '|-\n! Device ID !! Device Name !! Class !! Category !! PMA !! PMN\n'
            for a in range(0, 5):
                if pma_result_count > a:
                    new_content += '|-\n| [https://www.accessdata.fda.gov/scrIpts/cdrh/devicesatfda/index.cfm?db=pma&id='+str(pma_results[a][0])+' '+str(pma_results[a][0])+'] || '+str(pma_results[a][1])+' || '+str(pma_results[a][2])+' || '+str(pma_results[a][3])+' || True || False\n'
            for a in range(0, 5):
                if pmn_result_count > a:
                    new_content += '|-\n| [https://www.accessdata.fda.gov/scripts/cdrh/devicesatfda/index.cfm?db=pmn&id='+str(pmn_results[a][0])+' '+str(pmn_results[a][0])+'] || '+str(pmn_results[a][1])+' || '+str(pmn_results[a][2])+' || '+str(pmn_results[a][3])+' || False || True\n'
            new_content += '|}'
            # Add table to company description
            company_page_content = company_page_content.split("==Links==")
            company_page_content = company_page_content[0]+new_content+"\n==Links==\n"+company_page_content[1]
            # Update page
            print("Update page /index.php/"+company.replace(" ", "_"))
            # POST request to edit a page
            PARAMS_3 = {
                "action": "edit",
                "title": company,
                "token": CSRF_TOKEN,
                "format": "json",
                "text": company_page_content
            }
            R = S.post(URL, data=PARAMS_3)
            DATA = R.json()
            print(DATA)
            # Create Company_Name_FDA_Devices page with full list of devices
            print("Creating /index.php/"+company.replace(" ", "_")+"_FDA_Devices")
            devices_page_content = "This is an expanded list of medical devices registered with the FDA by [["+company+"]].\n"
            devices_page_content += "Find out more [[OpenFDA_Integration | here]].\n"
            devices_page_content += '{| class="wikitable" style="margin:auto"\n|+ FDA Approved Devices\n'
            devices_page_content += '|-\n! Device ID !! Device Name !! Class !! Category !! PMA !! PMN\n'
            for a in range(0, pma_result_count):
                if pma_result_count > a:
                    devices_page_content += '|-\n| [https://www.accessdata.fda.gov/scrIpts/cdrh/devicesatfda/index.cfm?db=pma&id='+str(pma_results[a][0])+' '+str(pma_results[a][0])+'] || '+str(pma_results[a][1])+' || '+str(pma_results[a][2])+' || '+str(pma_results[a][3])+' || True || False\n'
            for a in range(0, pmn_result_count):
                if pmn_result_count > a:
                    devices_page_content += '|-\n| [https://www.accessdata.fda.gov/scripts/cdrh/devicesatfda/index.cfm?db=pmn&id='+str(pmn_results[a][0])+' '+str(pmn_results[a][0])+'] || '+str(pmn_results[a][1])+' || '+str(pmn_results[a][2])+' || '+str(pmn_results[a][3])+' || False || True\n'
            devices_page_content += '|}'
            # POST request to create a page
            PARAMS_3 = {
                "action": "edit",
                "title": company+" FDA Devices",
                "token": CSRF_TOKEN,
                "format": "json",
                "text": devices_page_content
            }
            R = S.post(URL, data=PARAMS_3)
            DATA = R.json()
            print(DATA)

