'''
This script is used to fetch and parse RSS feeds.
'''

import feedparser

def arxiv_research(data_endpoint, requested_announce_type, requested_keywords):
    '''
    This function is used to fetch, parse and filter RSS feeds from arXiv.

    :param data_endpoint: The endpoint (category name with optional subcategory name) to 
    pass to the RSS feed link provided by arXiv.
    :param requested_announce_type: Research paper announce type to use in filtering RSS feeds.
    :param requested_keywords: Keywords (typed by user) to use in filtering RSS feeds.
    
    :return: Filtered entries of RSS feed.
    '''
    # url of the RSS feed
    url = f'https://rss.arxiv.org/rss/{data_endpoint}'

    # parse the RSS feed from the remote url
    feed = feedparser.parse(url)

    # get the status of the feed
    status = feed.get('status')

    # if status is not 200, raise an Exception
    # 200 stands for 'OK'; other status codes indicate an error
    if (status != 200):
        raise Exception(f'An error occured with status code={status}.')

    # get the entries of the feed
    entries = feed.get('entries')

    # to store filtered entries
    filtered_entries = []

    # iterate through the entries and filter them based on function parameters (announce type and keywords)
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
                
    # return the filtered entries
    return filtered_entries