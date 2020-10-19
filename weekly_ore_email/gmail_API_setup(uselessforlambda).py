import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient.discovery import build
#from weekly_ore_email.weekly_ore_email import refresh_access_token, get_credentials
import json
# god bless this guy https://medium.com/@ashokyogi5/a-beginners-guide-to-google -oauth-and-google-apis-450f36389184
CLIENT_SECRET = r"C:\Users\Alfredo\Downloads\client_secret_851645902441-edecpimieqffih4maorp6rudsns1dbfj.apps.googleusercontent.com.json"
SCOPE = ['https://www.googleapis.com/auth/drive.readonly',
         'https://www.googleapis.com/auth/gmail.send',
         'https://www.googleapis.com/auth/spreadsheets.readonly ']

print(SCOPE)
STORAGE = Storage('credentials_with_refresh.json')
#### RETRIEVE CREDENTIALS, WILL PROMPT TO BROWSER
credentials = STORAGE.get()
flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
http = httplib2.Http()
credentials = run_flow(flow, STORAGE, http=http) #stores with refresh toeken
print(credentials)

############
## access google drive
'''
creds = r':Users\Alfredo\weekly_ore_email_project\weekly_ore_email\credentials_with_refresh.json'
creds = json.loads(open(creds, 'r').read())
access = refresh_access_token(creds)
creds = get_credentials(access_token=access)
service = build('drive', 'v3', credentials=creds)
results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])


### USAGE
table = result['values']
[i for i in [j for j in table]]
#access birthday column
cols = table[0][0]
table[0].index('Cumpleaños del colaborador ')

'''