import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests
from datetime import datetime
CREDENTIALS_FILE = "Custom Analytics-3d262dd272bb.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ["https://www.googleapis.com/auth/spreadsheets",
                                                                                  "https://www.googleapis.com/auth/drive"])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build("sheets", "v4", http = httpAuth)

url = "http://steamcommunity.com/sharedfiles/filedetails/?id=1246109221"
r = requests.get(url)
soup = BeautifulSoup(r.text)
stats_table = soup.find("table",{"class": "stats_table"})
data = []
for row in stats_table.findAll("tr"):
    data.append(row.find("td").text)

main_table = service.spreadsheets().values().get(spreadsheetId="1-u7Bj2nYFM8LnUlDRH8sKhu27q1AkvGX4qVFcI4KMic", range = "Лист1!A2:C").execute()
values = main_table.get('values', [])

results = service.spreadsheets().values().batchUpdate(spreadsheetId = "1-u7Bj2nYFM8LnUlDRH8sKhu27q1AkvGX4qVFcI4KMic", body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "Лист1!A%s:E%s" % (len(values)+2, len(values)+2), 
         "majorDimension": "ROWS",     
         "values": [[data[0],data[1] ,data[2],datetime.strftime(datetime.now(), "%d.%m.%Y") ]]}
    ]
}).execute()
