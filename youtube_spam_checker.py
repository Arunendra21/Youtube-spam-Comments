import pandas as pd
import requests

API_KEY = 'AIzaSyDiutAD2Z15ZKMyL8jKjQSsTXYxouflAd0'

spam_keywords = [
    'subscribe', 'click here', 'buy now', 'free', 'giveaway',
    'visit my channel', 'earn money', 'check out', 'limited offer',
    'follow me', 'watch this', 'gift card', 'promotion', 'promo'
]

def get_video_id(url_or_id):
    if 'youtube.com' in url_or_id or 'youtu.be' in url_or_id:
        if 'v=' in url_or_id:
            return url_or_id.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in url_or_id:
            return url_or_id.split('youtu.be/')[1].split('?')[0]
    return url_or_id

def fetch_comments(video_id):
    comments = []
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?key={API_KEY}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=100"

    while url:
        response = requests.get(url).json()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
            url = f"https://www.googleapis.com/youtube/v3/commentThreads?key={API_KEY}&textFormat=plainText&part=snippet&videoId={video_id}&pageToken={next_page_token}&maxResults=100"
        else:
            url = None
    return comments

def is_spam(comment):
    for keyword in spam_keywords:
        if keyword.lower() in comment.lower():
            return True
    return False

def main():
    url_or_id = input("Enter YouTube Video Link or Video ID: ").strip()
    video_id = get_video_id(url_or_id)

    print("Fetching comments...")
    comments = fetch_comments(video_id)
    print(f"Fetched {len(comments)} comments.")

    df = pd.DataFrame(comments, columns=['Comment'])
    df['Is_Spam'] = df['Comment'].apply(is_spam)

    spam_comments = df[df['Is_Spam'] == True]

    print("\n🚨 Spam Comments Found:")
    print(spam_comments[['Comment']])

    save = input("\nDo you want to save spam comments to CSV? (y/n): ").lower()
    if save == 'y':
        spam_comments.to_csv(f"{video_id}_spam_comments.csv", index=False)
        print(f"Spam comments saved to {video_id}_spam_comments.csv")

if __name__ == "__main__":
    main()
