import json
import os

# load JSON data from airtable embedded here: https://neurotechx.com/neurotech-ecosystem/
content = open("test.json", "r", encoding="utf8").read()
jsoncontent = json.loads(content)

# Filter for brain-computer interface companies only
methods = ["BCI", "EEG", "ECG", "VNS", "Neurofeedback", "Biofeedback", "tDCS", "TMS", "MRI", "EOG",
           "Neuromodulation", "Light Stimulation", "Neurostimulation", "Neuromonitoring", "EMG", "Neural Interface",
           "DBS", "NIRS", "Brain Stimulation", "(ERP)", "FUS", "PET", "Optogenetics", "tACS", "FUS", "RNS", "CES", "EBS"]

for a in range(704, len(jsoncontent["data"]["table"]["rows"])): # Set range start value to save position
    company = jsoncontent["data"]["table"]["rows"][a]
    validcompany = False
    for b in range(0, len(methods)):
        if "fldRfohUfU2difvFP" in company["cellValuesByColumnId"] and 'fldJZX950vcXsaRGq' in company["cellValuesByColumnId"]: # if any methods are listed AND description is set
            if methods[b] in str(company["cellValuesByColumnId"]["fldRfohUfU2difvFP"]): # Find matching methods
                print(methods[b])
                validcompany = True
    if validcompany:
        # Create text content formatted for MediaWiki
        pagetext = "[[Category:Organizations]]\n[[Category:Companies]]\n"
        pagetext += company["cellValuesByColumnId"]["fldJZX950vcXsaRGq"] # description
        pagetext += "\n==Links=="
        website = company["cellValuesByColumnId"]["fldMw6GM44XBkSt8r"] # website
        if "http" not in company["cellValuesByColumnId"]["fldMw6GM44XBkSt8r"]:
            website = "http://"+company["cellValuesByColumnId"]["fldMw6GM44XBkSt8r"]
        pagetext += "\n["+website+" Website]"

        # Copy text to clipboard and open a new wiki page
        os.system('cmd /c "echo '+pagetext.replace("\n", "&echo ")+'" | clip')
        os.system("start https://bciwiki.org/index.php/"+company["cellValuesByColumnId"]["fldMKs6DSELmlMO70"].replace(" ", "%20"))
        input("=============== Row "+str(a)+" : "+str(round((a/len(jsoncontent["data"]["table"]["rows"]))*100, 2))+"% complete ===============")
