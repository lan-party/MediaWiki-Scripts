import requests
import os
import pyperclip

countries = {'UK': 'The United Kingdom', 'AF': 'Afghanistan', 'AL': 'Albania', 'DZ': 'Algeria', 'AS': 'American Samoa', 'AD': 'Andorra', 'AO': 'Angola', 'AI': 'Anguilla', 'AQ': 'Antarctica', 'AG': 'Antigua and Barbuda', 'AR': 'Argentina', 'AM': 'Armenia', 'AW': 'Aruba', 'AU': 'Australia', 'AT': 'Austria', 'AZ': 'Azerbaijan', 'BS': 'The Bahamas', 'BH': 'Bahrain', 'BD': 'Bangladesh', 'BB': 'Barbados', 'BY': 'Belarus', 'BE': 'Belgium', 'BZ': 'Belize', 'BJ': 'Benin', 'BM': 'Bermuda', 'BT': 'Bhutan', 'BO': 'Bolivia', 'BA': 'Bosnia and Herzegovina', 'BW': 'Botswana', 'BV': 'Bouvet Island', 'BR': 'Brazil', 'IO': 'British Indian Ocean Territory', 'BN': 'Brunei', 'BG': 'Bulgaria', 'BF': 'Burkina Faso', 'BI': 'Burundi', 'KH': 'Cambodia', 'CM': 'Cameroon', 'CA': 'Canada', 'CV': 'Cape Verde', 'KY': 'Cayman Islands', 'CF': 'Central African Republic', 'TD': 'Chad', 'CL': 'Chile', 'CN': 'China', 'CX': 'Christmas Island', 'CC': 'Cocos (Keeling) Islands', 'CO': 'Colombia', 'KM': 'Comoros', 'CG': 'The Congo', 'CD': 'Congo, the Democratic Republic of the', 'CK': 'Cook Islands', 'CR': 'Costa Rica', 'CI': 'Ivory Coast', 'HR': 'Croatia', 'CU': 'Cuba', 'CY': 'Cyprus', 'CZ': 'Czech Republic', 'DK': 'Denmark', 'DJ': 'Djibouti', 'DM': 'Dominica', 'DO': 'Dominican Republic', 'EC': 'Ecuador', 'EG': 'Egypt', 'SV': 'El Salvador', 'GQ': 'Equatorial Guinea', 'ER': 'Eritrea', 'EE': 'Estonia', 'ET': 'Ethiopia', 'FK': 'Falkland Islands (Malvinas)', 'FO': 'Faroe Islands', 'FJ': 'Fiji', 'FI': 'Finland', 'FR': 'France', 'GF': 'French Guiana', 'PF': 'French Polynesia', 'TF': 'French Southern Territories', 'GA': 'Gabon', 'GM': 'The Gambia', 'GE': 'Georgia', 'DE': 'Germany', 'GH': 'Ghana', 'GI': 'Gibraltar', 'GR': 'Greece', 'GL': 'Greenland', 'GD': 'Grenada', 'GP': 'Guadeloupe', 'GU': 'Guam', 'GT': 'Guatemala', 'GG': 'Guernsey', 'GN': 'Guinea', 'GW': 'Guinea-Bissau', 'GY': 'Guyana', 'HT': 'Haiti', 'HM': 'Heard Island and McDonald Islands', 'VA': 'Holy See (Vatican City State)', 'HN': 'Honduras', 'HK': 'Hong Kong', 'HU': 'Hungary', 'IS': 'Iceland', 'IN': 'India', 'ID': 'Indonesia', 'IR': 'Iran, Islamic Republic of', 'IQ': 'Iraq', 'IE': 'Ireland', 'IM': 'Isle of Man', 'IL': 'Israel', 'IT': 'Italy', 'JM': 'Jamaica', 'JP': 'Japan', 'JE': 'Jersey', 'JO': 'Jordan', 'KZ': 'Kazakhstan', 'KE': 'Kenya', 'KI': 'Kiribati', 'KP': "Korea, Democratic People's Republic of", 'KR': 'South Korea', 'KW': 'Kuwait', 'KG': 'Kyrgyzstan', 'LA': "Lao People's Democratic Republic", 'LV': 'Latvia', 'LB': 'Lebanon', 'LS': 'Lesotho', 'LR': 'Liberia', 'LY': 'Libya', 'LI': 'Liechtenstein', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'MO': 'Macao', 'MK': 'Macedonia, the former Yugoslav Republic of', 'MG': 'Madagascar', 'MW': 'Malawi', 'MY': 'Malaysia', 'MV': 'The Maldives', 'ML': 'Mali', 'MT': 'Malta', 'MH': 'Marshall Islands', 'MQ': 'Martinique', 'MR': 'Mauritania', 'MU': 'Mauritius', 'YT': 'Mayotte', 'MX': 'Mexico', 'FM': 'Micronesia, Federated States of', 'MD': 'Moldova, Republic of', 'MC': 'Monaco', 'MN': 'Mongolia', 'ME': 'Montenegro', 'MS': 'Montserrat', 'MA': 'Morocco', 'MZ': 'Mozambique', 'MM': 'Burma', 'NA': 'Namibia', 'NR': 'Nauru', 'NP': 'Nepal', 'NL': 'The Netherlands', 'AN': 'Netherlands Antilles', 'NC': 'New Caledonia', 'NZ': 'New Zealand', 'NI': 'Nicaragua', 'NE': 'Niger', 'NG': 'Nigeria', 'NU': 'Niue', 'NF': 'Norfolk Island', 'MP': 'Northern Mariana Islands', 'NO': 'Norway', 'OM': 'Oman', 'PK': 'Pakistan', 'PW': 'Palau', 'PS': 'Palestinian Territory, Occupied', 'PA': 'Panama', 'PG': 'Papua New Guinea', 'PY': 'Paraguay', 'PE': 'Peru', 'PH': 'Philippines', 'PN': 'Pitcairn', 'PL': 'Poland', 'PT': 'Portugal', 'PR': 'Puerto Rico', 'QA': 'Qatar', 'RE': 'Réunion', 'RO': 'Romania', 'RU': 'Russia', 'RW': 'Rwanda', 'SH': 'Saint Helena, Ascension and Tristan da Cunha', 'KN': 'Saint Kitts and Nevis', 'LC': 'Saint Lucia', 'PM': 'Saint Pierre and Miquelon', 'VC': 'St. Vincent and the Grenadines', 'WS': 'Samoa', 'SM': 'San Marino', 'ST': 'Sao Tome and Principe', 'SA': 'Saudi Arabia', 'SN': 'Senegal', 'RS': 'Serbia', 'SC': 'Seychelles', 'SL': 'Sierra Leone', 'SG': 'Singapore', 'SK': 'Slovakia', 'SI': 'Slovenia', 'SB': 'The Solomon Islands', 'SO': 'Somalia', 'ZA': 'South Africa', 'GS': 'South Georgia and the South Sandwich Islands', 'SS': 'South Sudan', 'ES': 'Spain', 'LK': 'Sri Lanka', 'SD': 'Sudan', 'SR': 'Suriname', 'SJ': 'Svalbard and Jan Mayen', 'SZ': 'Swaziland', 'SE': 'Sweden', 'CH': 'Switzerland', 'SY': 'Syrian Arab Republic', 'TW': 'Taiwan', 'TJ': 'Tajikistan', 'TZ': 'Tanzania, United Republic of', 'TH': 'Thailand', 'TL': 'Timor-Leste', 'TG': 'Togo', 'TK': 'Tokelau', 'TO': 'Tonga', 'TT': 'Trinidad and Tobago', 'TN': 'Tunisia', 'TR': 'Turkey', 'TM': 'Turkmenistan', 'TC': 'Turks and Caicos Islands', 'TV': 'Tuvalu', 'UG': 'Uganda', 'UA': 'Ukraine', 'AE': 'United Arab Emirates', 'GB': 'United Kingdom', 'US': 'The United States', 'UM': 'United States Minor Outlying Islands', 'UY': 'Uruguay', 'UZ': 'Uzbekistan', 'VU': 'Vanuatu', 'VE': 'Venezuela', 'VN': 'Vietnam', 'VG': 'Virgin Islands, British', 'VI': 'The Virgin Islands, U.S.', 'WF': 'Wallis and Futuna', 'EH': 'Western Sahara', 'YE': 'Yemen', 'ZM': 'Zambia', 'ZW': 'Zimbabwe'}
savestate = 0


# Collect categorized company data
resp = requests.get("https://bciwiki.org/index.php/Category:Companies").text
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
            names = companyinfo[b].split('<a href="')[1:]
            name = ""
            for n in names:
                n = n.split('"')[0]
                if len(names) > 1:
                    n = " "+n.split("/")[2]+","
                else:
                    n = n.split("/")[2]
                name += n
            if len(names) > 1:
                name = name[:-1]
            allcompanyinfo[allcompanyindex] += [name]
        else:
            info = companyinfo[b].split("\\n</td>")[0]
            allcompanyinfo[allcompanyindex] += [info]
        if b == 11:
            allcompanyindex += 1
            allcompanyinfo += [[]]
allcompanyinfo.pop()
print(len(allcompanyinfo))

# Generate pagetext additions for each company
for a in range(savestate, len(allcompanyinfo)):
    companyinfo = allcompanyinfo[a]
    
    # Infographic link, country and year founded
    pagetext = "\n\n\n[[File:"+companyinfo[0]+".png|thumb|"+companyinfo[0].replace("_", " ")+" Company Profile]]\n"
    pagetext += "Founded in "+countries[companyinfo[5]]+" around "+companyinfo[6]+", "+companyinfo[0].replace("_", " ")+" produces "
    
    # Hardware and software 
    truecount = 0
    if companyinfo[1] == 'True':
        pagetext += "noninvasive hardware, "
        truecount += 1
    if companyinfo[2] == 'True':
        pagetext += "invasive hardware, "
        truecount += 1
    if companyinfo[3] == 'True':
        pagetext += "end-user software, "
        truecount += 1
    if companyinfo[4] == 'True':
        pagetext += "developer tools"
        truecount += 1
    if companyinfo[1] == 'False' and companyinfo[2] == 'False' and companyinfo[3] == 'False' and companyinfo[4] == 'False':
        pagetext += "neurotech consulting services"
        
    if pagetext[-2:] == ", ":
        pagetext = pagetext[::-1].replace(" ,", "\n\n.", 1)[::-1]
    else:
        pagetext += ".\n\n"
        
    if truecount > 1:
        pagetext = pagetext[::-1].replace(" ,", " dna ", 1)[::-1]
    
    # Application Categories
    pagetext += companyinfo[0].replace("_", " ")+" makes tools for "
    truecount = 0
    if 'Clinical' in companyinfo[7]:
        pagetext += "medical diagnosis and treatment through body/mind state interpretation and/or neurostimulation therapies, "
        truecount += 1
    if 'RC/UI' in companyinfo[7]:
        pagetext += "the assisted control of mechanical,electrical,and digital devices/applications, "
        truecount += 1
    if 'Subjective Measurement' in companyinfo[7]:
        pagetext += "the objective measurement of subjective experiences through mind/body state interpretation, "
        truecount += 1
    if 'Motor-Sensory Augmentation' in companyinfo[7]:
        pagetext += "feedback through neurostimulation techniques, "
        truecount += 1
    if 'Wetwear Computing' in companyinfo[7]:
        pagetext += "the sensing and stimulation of biological neural networks, either within an animal or grown in a dish, to perform calculations"
        truecount += 1

    if pagetext[-2:] == ", ":
        pagetext = pagetext[::-1].replace(" ,", "\n\n.", 1)[::-1]
    else:
        pagetext += ".\n\n"
        
    if truecount > 1:
        pagetext = pagetext[::-1].replace(" ,", " dna ", 1)[::-1]
    
    # BCI categories
    pagetext += "[[Brain Computer Interface Classification|BCI Categories]]: "
    truecount = 0
    if 'Open-Loop Efferent' in companyinfo[8]:
        pagetext += 'Open-Loop Efferent, '
        truecount += 1
    if 'Open-Loop Afferent' in companyinfo[8]:
        pagetext += 'Open-Loop Afferent, '
        truecount += 1
    if 'Closed-Loop Efferent' in companyinfo[8]:
        pagetext += 'Closed-Loop Efferent, '
        truecount += 1
    if 'Closed-Loop Afferent' in companyinfo[8]:
        pagetext += 'Closed-Loop Afferent, '
        truecount += 1
    if 'Bidirectional Afferent Closed-Loop' in companyinfo[8]:
        pagetext += 'Bidirectional Afferent Closed-Loop, '
        truecount += 1

    pagetext = pagetext[::-1].replace(" ,", "", 1)[::-1]
    
    # Neurostim and imaging techniques
    if companyinfo[9] != "":
        pagetext += "\n\n[[:Category:Neurosensing_Techniques|Neurosensing Technique(s)]]: "+companyinfo[9]
    if companyinfo[10] != "":
        pagetext += "\n\n[[:Category:Neurostimulation_Techniques|Neurostimulation Technique(s)]]: "+companyinfo[10]

    # Copy pagetext addition to clipboard and open company page in browser
    resp = str(requests.get("https://bciwiki.org/index.php?title="+companyinfo[0].replace(" ", "%_")+"&action=edit").content)
    if "Category:Neurosensing_Techniques" not in resp and "Category:Neurostimulation_Techniques" not in resp:
        pyperclip.copy(pagetext)
        os.system("start https://bciwiki.org/index.php/"+companyinfo[0].replace(" ", "%20"))
        print(str(a)+" - "+str(a/len(allcompanyinfo)*100)+"%")
        input(pagetext)
