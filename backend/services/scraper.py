import random

def fetch_tweets(hashtag, limit=100):
    """
    Mock implementation of fetch_tweets since snscrape is broken by Twitter API changes.
    Generates realistic looking tweets related to the hashtag.
    """
    tweets = []
    
    # Common positive phrases
    positive = [
        f"Just discovered #{hashtag} and it's absolutely amazing! Highly recommend.",
        f"The progress in #{hashtag} lately is mind-blowing. Love seeing this grow.",
        f"Can't get enough of #{hashtag}! Best thing on my feed today.",
        f"I'm so excited about the future of #{hashtag}. Great community!",
        f"Finally understanding #{hashtag} and it feels great. 🌟"
    ]
    
    # Common neutral phrases
    neutral = [
        f"Does anyone have good resources for learning about #{hashtag}?",
        f"Reading up on #{hashtag} this morning. Lots of information.",
        f"Currently looking into #{hashtag}. Interesting stuff.",
        f"What are your thoughts on #{hashtag}? Let me know below.",
        f"Just a regular day exploring #{hashtag}."
    ]
    
    # Common negative phrases
    negative = [
        f"Really frustrated with how #{hashtag} is being handled right now.",
        f"I don't understand the hype around #{hashtag}. Seems overrated.",
        f"Having so many issues with #{hashtag} today. Very annoying.",
        f"Disappointed by the recent news regarding #{hashtag}.",
        f"Is anyone else sick of hearing about #{hashtag}?"
    ]
    
    # Pool of all phrases to sample from
    pool = positive + positive + neutral + negative # Skew positive logically
    
    # Generate tweets up to the requested limit (or realistic max)
    actual_limit = min(limit, random.randint(15, 80)) # Return a realistic number of 'found' tweets
    
    for i in range(actual_limit):
        text = random.choice(pool)
        
        # Add some random variations to make them look distinct
        if random.random() > 0.5:
            text += f" #{hashtag}"
        if random.random() > 0.8:
            text = text.upper()
            
        tweets.append({
            "text": text,
            "media": None # Media mock can be added if needed later
        })
        
    return tweets
