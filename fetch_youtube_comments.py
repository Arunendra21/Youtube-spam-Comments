from googleapiclient.discovery import build
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
api_key = os.getenv("API_KEY")

youtube = build('youtube', 'v3', developerKey=api_key)
video_id = '1Jj4T_HKSQE'
comments = []

request = youtube.commentThreads().list(
    part='snippet',
    videoId=video_id,
    maxResults=100,
    textFormat="plainText"
)
response = request.execute()

for item in response['items']:
    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
    comments.append(comment)

df = pd.DataFrame(comments, columns=['Comment'])
df.to_csv('youtube_comments.csv', index=False)

print("Comments have been saved to youtube_comments.csv!")
