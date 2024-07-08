import feedparser
from category_mapping import arxiv_mapping

def arxiv_research(category):
    category_abbreviation = arxiv_mapping.get(category)
    url = f'https://rss.arxiv.org/rss/{category_abbreviation}'

    feed = feedparser.parse(url)
    entries = feed.get('entries')

    return entries