import feedparser
from category_mapping import arxiv_mapping

def arxiv_research(category):
    arxiv_category = arxiv_mapping.get(category)

    url = f'https://rss.arxiv.org/rss/{arxiv_category}'

    feed = feedparser.parse(url)

    print(feed)

if __name__ == "__main__":
    arxiv_research('Computer Science')