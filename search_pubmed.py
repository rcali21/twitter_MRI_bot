# pubmed_search.py

import os
from Bio import Entrez
from datetime import datetime, timedelta
import time

def search_pubmed():
    # get environment variables as ENTREZ_EMAIL
    
    Entrez.email = os.environ.get('ENTREZ_EMAIL')

    # Calculate today's and yesterday's dates in the YYYY/MM/DD format
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    today_str = today.strftime("%Y/%m/%d")
    yesterday_str = yesterday.strftime("%Y/%m/%d")

    # Define your primary and secondary topics
    primary_topics = ["MRI", "magnetic resonance imaging", "neuroimaging"]
    secondary_topics = [
        "diffusion", "diffusion imaging", "dmri", "fMRI", "DWI", "DTI",
        "anatomical MRI", "T1w", "brain MRI", "functional imaging",
        "pulse sequence", "deep learning", "machine learning", "segmentation",
        "automated", "labeling", "computer vision", "MPRAGE", "SPGR",
        "perfusion","ASL","PCASL","time of flight", "tof","MEMPRAGE", 
        "brain imaging", "SWI", "susceptibility weighted imaging", "T2w", "T2*"
    ]

    articles = []

    # Fetch the results for each combination of topics
    for primary in primary_topics:
        for secondary in secondary_topics:
            query = f"(({primary}[Title/Abstract]) AND {secondary}[Title/Abstract]) AND (\"{yesterday_str}\"[Date - Publication] : \"{today_str}\"[Date - Publication])"

            handle = Entrez.esearch(db="pubmed", term=query)
            record = Entrez.read(handle)
            handle.close()

            id_list = record["IdList"]
            time.sleep(1)  # wait for 1 second to avoid hitting rate limits

            for id in id_list:
                handle = Entrez.esummary(db="pubmed", id=id)
                record = Entrez.read(handle)
                handle.close()

                title = record[0]['Title']
                try:
                    doi = record[0]['ArticleIds']['doi']
                    articles.append(f"Title: {title}\nDOI: https://doi.org/{doi}")
                except KeyError:
                    articles.append(f"Title: {title}\nDOI: Not available")

                time.sleep(1)  # wait for 1 second to avoid hitting rate limits

    # Convert to a set to remove duplicates, then back to a list
    articles = list(set(articles))

    return articles

if __name__ == "__main__":
    articles = search_pubmed()
    for article in articles:
        print(article)
        print()