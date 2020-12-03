
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

credentials = None

# token.picle stores the user's credentials from previously successful logins
if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

# If there are no valid credentials available, then either refresh teh tokekn or log in
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing Access Token...")
        credentials.refresh(Request())
    else:
        print("Fetching New Tokens...")
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secrets.json",
            scopes=["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.channel-memberships.creator"]
        )
        
        flow.run_local_server(
            port=8080, prompt="consent", authorization_prompt_message=''
        )
        credentials = flow.credentials

        with open("token.pickle", "wb") as f:
            print("Saving Credentials for Future Use...")
            pickle.dump(credentials, f)


youtube = build("youtube", "v3", credentials=credentials)
print("\nStart of script...")
print("clear next_page_token")

sub_count = int(0)
nextPageToken = None

while True:

    request = youtube.subscriptions().list(
        part="subscriberSnippet",
        #myRecentSubscribers = True,
        mySubscribers=True,
        maxResults=50,
        order = "alphabetical",
        pageToken=nextPageToken
    )

    response = request.execute()
 

    for item in response['items']:
        sub_count += 1
        print(sub_count, item["subscriberSnippet"]["title"])
    #    user_name = item["subscriberSnippet"]["title"]
    #    yt_link = f"Channel Name - {user_name}"

    print("Set next_page_token")
    next_page_token = response['nextPageToken']

    if sub_count > 150 :
        break


    print("This is the end...\n\n")
    nextPageToken = response.get('nextPageToken')
    if not nextPageToken:
        break
