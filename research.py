import feedparser

def arxiv_research(category='cs'):
    url = f'https://rss.arxiv.org/rss/{category}'

    feed = feedparser.parse(url)

    print(feed)

if __name__ == "__main__":
    arxiv_research()