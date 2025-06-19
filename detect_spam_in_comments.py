import pandas as pd

df = pd.read_csv('youtube_comments.csv')

print(df.head())

spam_keywords = [
    'subscribe', 'click here', 'buy now', 'free', 'giveaway', 
    'visit my channel', 'earn money', 'check out', 'limited offer',
    'follow me', 'watch this', 'gift card', 'promotion', 'promo'
]

def is_spam(comment):
    for keyword in spam_keywords:
        if keyword.lower() in comment.lower():
            return True
    return False

df['Is_Spam'] = df['Comment'].apply(is_spam)

df.to_csv('youtube_comments_with_spam.csv', index=False)

print("Spam detection completed and saved to youtube_comments_with_spam.csv!")
spam_comments = df[df['Is_Spam'] == True]
print(spam_comments)

spam_comments.to_csv('spam_only_comments.csv', index=False)

