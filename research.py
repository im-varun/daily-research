import feedparser

def arxiv_research(data_endpoint):
    url = f'https://rss.arxiv.org/rss/{data_endpoint}'

    feed = feedparser.parse(url)
    entries = feed.get('entries')

    return entries