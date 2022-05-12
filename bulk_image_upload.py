import requests
import os

# List of files to upload from directory listing
filelist = os.listdir("uploadprofiles")

# Session and wpEditToken are updated regularly by MediaWiki
# Retrieve from header and POST parameters sent by the browser on a save page request
session = "***"
edittoken = "***"
wikitoken = "***"

# Upload all images with generated descriptions
for filename in filelist:
    companyname = filename.split(".")[0]
    companyname = companyname.replace("_", " ")
    description = "Company profile infographic for "+companyname
    print("[[File:"+filename+"|frameless|caption]]")
    profile_img = open("uploadprofiles\\"+filename, "rb")
    resp = requests.post("https://bciwiki.org/index.php/Special:Upload", params={
        "wpDestFile": filename,
        "wpUploadDescription": description,
        "wpLicense": "",
        "wpWatchthis": "1",
        "wpEditToken": edittoken,
        "title": "Special:Upload",
        "wpDestFileWarningAck": "",
        "wpForReUpload": "1",
        "wpUpload": "Upload file",
        "wpUpload": "Upload file"}, files={"wpUploadFile": profile_img}, cookies={
                    "ls_smartpush": "1",
                    "mw_installer_session": "",
                    "u216253868_bciwiki_session": session,
                    "u216253868_bciwikiToken": wikitoken,
                    "u216253868_bciwikiUserID": "1",
                    "u216253868_bciwikiUserName": "Landonodnal",
                    "VEE": "wikitext",
                    "wikiEditor-0-toolbar-section": "advanced"
            })
    profile_img.close()
    print(filename)
    print(resp.ok)
