# main.py

import time
import os
from search_pubmed import search_pubmed
from post_tweet import post_tweet

if __name__ == "__main__":
    ENTREZ_EMAIL = os.environ.get('ENTREZ_EMAIL')
    if not ENTREZ_EMAIL:
        raise Exception("Entrez Email not found in environment variables.")
    
    articles = search_pubmed()

    for article in articles:
        post_tweet(article)
        time.sleep(300)  # Wait for 5 minutes (300 seconds) before posting the next tweet
