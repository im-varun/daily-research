import feedparser

def arxiv_research(category_abbreviation):
    url = f'https://rss.arxiv.org/rss/{category_abbreviation}'

    feed = feedparser.parse(url)
    entries = feed.get('entries')

    return entries