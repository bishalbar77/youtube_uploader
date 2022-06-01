import os
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def add_to_playlist(videoId, playlistId):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    creds=0
    # Get credentials and create an API client
    if os.path.exists('playtoken.json'):
        creds = Credentials.from_authorized_user_file('playtoken.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('playtoken.json', 'w') as token:
            token.write(creds.to_json())
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    request = youtube.playlistItems().insert(
        part="snippet,id",
        body={
          "snippet": {
            "playlistId": playlistId,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": videoId
            }
        }

        }
    )
    response = request.execute()
    print(response)
