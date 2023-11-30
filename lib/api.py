import os
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def Api(idYT:str):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    apiKey = "AIzaSyDXY3jDM8rf8PyhJL7XGlxUh4kEIp6cCWY"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=apiKey)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=idYT
    )
    response = request.execute()
    
    channelId = response['items'][0]['snippet']['channelId']
    
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channelId
    )
    
    resp = request.execute()
    
    data = [
            response['items'][0]['snippet']['title'], 
            response['items'][0]['snippet']['channelTitle'],
            response['items'][0]['statistics']['viewCount'],
            response['items'][0]['snippet']['publishedAt'],
            response['items'][0]['snippet']['thumbnails']['standard']['url'],
            resp['items'][0]['snippet']['thumbnails']['medium']['url']
        ]
    
    # with open('response.json', 'w') as res:
    #     json.dump(response, res)

    return data
