'''
This script is used to fetch and parse RSS feeds.
'''

import feedparser

def arxiv_research(data_endpoint, requested_announce_type, requested_keywords):
    '''
    This function is used to fetch, parse and filter RSS feeds from arXiv.
    :param data_endpoint: The endpoint (category name with optional subcategory name) to 
    pass to the RSS feeds link provided by arXiv.
    :param requested_announce_type: Research paper announce type to use in filtering RSS feeds.
    :param requested_keywords: Keywords (typed by user) to use in filtering RSS feeds.
    '''
    url = f'https://rss.arxiv.org/rss/{data_endpoint}'

    feed = feedparser.parse(url)

    status = feed.get('status')

    if (status != 200):
        raise Exception(f'An error occured with status code={status}.')

    entries = feed.get('entries')

    filtered_entries = []

    for entry in entries:
        announce_type = entry.get('arxiv_announce_type')
        if (requested_announce_type == 'all') or (requested_announce_type == announce_type):
            if (len(requested_keywords) != 0):
                title = entry.get('title')

                summary = entry.get('summary')
                abstract = summary[summary.index('Abstract'):]

                if any((keyword in title) or (keyword in abstract) for keyword in requested_keywords):
                    filtered_entries.append(entry)
            else:
                filtered_entries.append(entry)
                

    return filtered_entries