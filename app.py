import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()


API_KEY = os.getenv("API_KEY")
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
    st.title("🎥 YouTube Spam Comment Detector")

    st.write("Enter a YouTube Video Link or Video ID below 👇")

    url_or_id = st.text_input("Video Link or ID")

    if st.button("Detect Spam Comments"):
        if url_or_id:
            with st.spinner('Fetching comments...'):
                video_id = get_video_id(url_or_id)
                comments = fetch_comments(video_id)

                if len(comments) == 0:
                    st.error("No comments found or invalid video ID.")
                    return

                df = pd.DataFrame(comments, columns=['Comment'])
                df['Is_Spam'] = df['Comment'].apply(is_spam)

                spam_comments = df[df['Is_Spam'] == True]

                st.success(f"Fetched {len(comments)} comments. Found {len(spam_comments)} spam comments.")
                st.subheader("🚨 Spam Comments")
                st.dataframe(spam_comments[['Comment']])

                # Allow download
                csv = spam_comments.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Spam Comments as CSV",
                    data=csv,
                    file_name=f"{video_id}_spam_comments.csv",
                    mime='text/csv'
                )
        else:
            st.warning("Please enter a video link or ID.")

if __name__ == "__main__":
    main()
